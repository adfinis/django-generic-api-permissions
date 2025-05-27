# Django Generic API Permissions

Django Generic API Permissions (DGAP) is a framework to make your Django Rest
Framework API user-extensible for common use cases. Specifically, it provides
a simple API for your users to define specific visibilities, permissions, and
validations.

Assume you have an API service that implements a blogging backend. You have
a `Post`, and a `Comment` model.

When deployed as a public blog, you want admins users to be able to post, and
authenticated users be able to comment. Everybody is allowed to read posts and
comments.

But the same software should also be used in a company-internal deployment where
the rules are different: Anonymous users should not see anything, and you have
specific rules as to who can write posts.

DGAP makes it easy to implement the blog once, and make the permissions,
visibilities, and validations custom to each deployment.

## Concepts

DGAP provides you with three configuration settings: Visibilities, Permissions,
and Validations.

- The **visibilities** are run when getting data from the API. They define, on a
  per-user base, who can see which data.
- The **validations** are run on create and update operations, so
  data can be checked and modified before the update takes place.
- The **permissions** then define what a user can do with a given (visible) piece of
  data.

## Installation for app developers

If you want to integrate DGAP into your app, these are the steps you need.
Install DGAP (and add to your requirements files etc) first.

```bash
pip install django-generic-api-permissions
```

Then, add `generic_permissions.apps.GenericPermissionsConfig` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    "generic_permissions.apps.GenericPermissionsConfig",
    ...
)
```

### Visibility subsystem

The visibility part defines what you can see at all. Anything you cannot
see, you're implicitly also not allowed to modify. The visibility classes
define what you see depending on your roles, permissions, etc. Building
on top of this follow the permission classes (see below) that define
what you can do with the data you see.

For the visibilities, extend your DRF `ViewSet` classes with the
`VisibilityViewMixin`:

```python
# views.py
from rest_framework.viewsets import ModelViewSet
from generic_permissions.visibilities import VisibilityViewMixin
class MyModelViewset(VisibilityViewMixin, ModelViewSet):
    serializer_class = MyModelSerializers
    queryset = ...
```

Data leaks in REST Framework may happen if you use includes (or even only references) from a model the user may see to something that should be hidden.
To avoid such leaks, make sure to use a subclassed related field (either by creating your own using the provided `VisibilityRelatedFieldMixin`, or by using one of the provided types. See example below).
To set it for every relation in the serializer use DRFs `serializer_related_field` attribute in the serializer.

It's important to be aware of potential issues when updating (PATCH) existing relationships, especially when some relationships are hidden due to visibility settings. If not handled correctly, the hidden relationships may be unintentionally removed during an update, resulting in only the new relationships being set.

To avoid this, you must incorporate the `VisibilitySerializerMixin` into your serializer where you're using the `VisibilityRelatedFieldMixin` for the relationship field. This ensures that hidden relationships are properly accounted for during updates.

Remember to define the `VisibilitySerializerMixin` after the `ValidatorMixin`. This order is crucial because it ensures that validations are performed first, and only then are the relationships updated.

This step is vital to maintain the integrity of your data and prevent accidental loss of hidden relationships.

```python
# serializers.py
from rest_framework.viewsets import ModelSerializer
from generic_permissions.visibilities import VisibilityPrimaryKeyRelatedField, VisibilitySerializerMixin
class MyModelSerializers(VisibilitySerializerMixin, ModelSerializer):
    serializer_related_field = VisibilityPrimaryKeyRelatedField
```

A few subclassed fields are provided for different types of `RelatedField`:

- `VisibilityPrimaryKeyRelatedField`
- `VisibilityResourceRelatedField`
- `VisibilitySerializerMethodResourceRelatedField`

If a different relation field variation is needed extend it with `VisibilityRelatedFieldMixin`:

```python
from generic_permissions.visibilities import VisibilityRelatedFieldMixin
class CustomRelationField(VisibilityRelatedFieldMixin):
    pass
```

#### Bypassing visibilities for foreign keys for 1:n and n:m

DGAP allows you to enforce visibility checks on foreign keys as well. Sometimes, you might want to bypass this, as it's not always necessary. For example, if you have a "document" with multiple "versions" as a 1:n relationship, you don't want to filter the versions queryset again, as it conforms to the same rules as the documents (that you 've already filtered)

To configure this, add the following key to your `settings.py`:

```python
GENERIC_PERMISSIONS_BYPASS_VISIBILITIES = {
    "my_app.Document": ["versions"], # attribute name as defined on the model
    "my_app.File": "__all__" # for all fields
}
```

Only use `__all__` for testing or if you're sure that you are not accidentally exposing any related models.

### Permission subsystem

Similarly, for the permissions system, add the `PermissionViewMixin` to your
views:

```python
# views.py
from rest_framework.viewsets import ModelViewSet
from generic_permissions.permissions import PermissionViewMixin
class MyModelViewset(PermissionViewMixin, VisibilityViewMixin, ModelViewSet):
    serializer_class = ...
    queryset = ...
```

You may use only one of the two mixins, or both, depending on your needs.

### Validation subsystem

Last, for the validation system, you extend your **serializer** with a mixin:

```python
# serializers.py
from rest_framework.serializers import ModelSerializer

from generic_permissions.serializers import PermissionSerializerMixin
from generic_permissions.validation import ValidatorMixin

from myapp import models

class MyModelSerializer(ValidatorMixin, ModelSerializer):
    # my field definitions...
    class Meta:
        model = models.MyModel
        fields = "__all__"
```

## Usage - for people deploying a DGAP-equipped app

Say you have an blog you want to deploy that uses DGAP. You want public blog
posts, but the comment section should only be visible for authenticated users.
For this, you would define a custom visibility class that limits access
accordingly.

### Visibilities

First, let's define the visibility class:

```python
# my_custom_visibilities.py
from generic_permissions.visibilities import filter_queryset_for
from my_app.models import Post, Comment

class CustomVisibility:
    @filter_queryset_for(Post)
    def filter_posts(self, queryset, request):
        # no filtering on blog posts
        return queryset
    @filter_queryset_for(Comment)
    def filter_comments(self, queryset, request):
        # Only authenticated users shall see comments
        if request.user.is_authenticated:
            return queryset
        else:
            return queryset.none()
```

Once done, open `settings.py` and point the `GENERIC_PERMISSIONS_VISIBILITY_CLASSES`
setting to the class you just defined. It is a list of strings that name the
visibility classes.

```python
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = ['my_custom_visibilities.CustomVisibility']
```

Note: The setting may be defined using env variables depending on the
project. In that case, set the value via that way instead.

Some times, you have visibilities that you want to combine: Say one visibility
class provides read access for user group A, another class provides access for
user group B. You want to combine those in a simple way. For this, we have
provided you the `Union` visibility:

```python
from generic_permissions.visibilities import Union

class MyFirstVisibility:
    #  ...
class MySecondVisibility:
    #  ...

class ResultingVisibility(Union):
    # Define a property `visibility_classes`. Those
    # will then be checked both, and if either one allows
    # an object to be seen, it will be visible to the user.
    visibility_classes = [MyFirstVisibility, MySecondVisibility]
```

### Permissions

Permission classes define who may perform which data mutation. They can be configured
via `GENERIC_PERMISSIONS_PERMISSION_CLASSES`.

To write custom permission classes, you create a simple class, and decorate the
methods that define the permissions accordingly.

There are two types of methods in the permissions system:

- `permission_for`: Marks methods that define generic access permissions for a
  given model. They are always checked first.
  Those methods will receive one positional argument, namely the `request` object
- `object_permission_for`: Define whether access to a specific object shall be
  granted. This called for all other operations **except** creation.
  These methods will receive two positional arguments: First, the `request`
  object, and second, the model instance that is being accessed in the request.

The following example carries on the Blog concept from above. We want only
admins to edit/update blog posts, and authenticated users to comment.
Nobody should be able to edit their comments.

We also show the concept of combining two permission classes here. DGAP looks at
the whole inheritance tree to figure out the permissions, so you can leverage
that to avoid code duplication.

You can find more information about the `request` object in the
[Django documentation](https://docs.djangoproject.com/en/3.1/ref/request-response/#httprequest-objects)

```python
from generic_permissions.permissions import permission_for, object_permission_for
from my_app.models import Post, Comment

class OnlyAuthenticated:
    @permission_for(object)
    def has_permission_default(self, request):
        # No permission is granted for any non-authenticated users
        return request.user.is_authenticated

class BlogPermissions:
    @permission_for(Comment)
    def has_permission_for_comment(self, request):
        # comments can be added, but not updated
        return request.method == 'POST'
    @permission_for(Post)
    def has_permission_for_post(self, request, instance):
        # Only admins can work on Posts
        return 'admin' in request.user.groups
    @object_permission_for(Post)
    def has_object_permission_for_post(self, request, instance):
        # Of the admins, changing a Post is only allowed to the author.
        return instance.author == request.user
```

The following pre-defined classes are available:

- `generic_permissions.permissions.AllowAny`: allow any users to perform any mutation (default)
- `generic_permissions.permissions.DenyAll`: deny all operations to any object.
  You can use this as a base class for your permissions - as long as you don't
  allow something, it will be denied.

### Data validation

Once the permission to access or modify an object is granted, you may want to
apply some custom validation as well.

In the example we're using here, we assume some user registration form. We want to
ensure that the username contains only lowercase letters.

For this, you can use the `GENERIC_PERMISSIONS_VALIDATION_CLASSES` setting. The settings is a
list of strings, representing a list of class names).

Here's an example validator class that ensures the username is lower case.

```python
from generic_permissions.validation import validator_for
from my_app.models import User

class LowercaseUsername:
    @validator_for(User)
    def lowercase_username(self, data, context):
        data["username"] = data["username"].lower()
        return data
```

The `@validator_for` decorator tells DGAP that the method shall
be called when a `User` is modified. The data passed in is already
parsed and validated by the REST framework, and it is expected that
the method returns a `dict` with a compatible structure. You may also
`raise ValidationError("some message")` if you don't want the validation
to succeed.
The second parameter, `context`, is a `dict` containing the DRF context: Access
`context['request']` to get the request (if validation depends on the user,
for example).
