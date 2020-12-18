# Django Generic API Permissions

Django Generic API Permissions supports you to implement generic APIs that can be used in different contexts.

In such scenario, you might want to define different sets of permissions and visibilities per
project. Django Generic API Permissions allows for creating custom permission and visibility
classes, where you can describe the desired setup with code.

## Installation

```
pip install django-generic-api-permissions
```

## Usage

In the `tests` directory you can find a simple example project demonstrating the usage
of Django Generic API Permissions.

Add `generic_permissions.apps.GenericPermissionsConfig` to your `INSTALLED_APPS`:

```
INSTALLED_APPS = (
    ...
    "generic_permissions.apps.GenericPermissionsConfig",
    ...
)
```

### Visibility

The visibility part defines what you can see at all. Anything you cannot see, you're
implicitly also not allowed to modify. The visibility classes define what you see
depending on your roles, permissions, etc. Building on top of this follow the permission
classes (see below) that define what you can do with the data you see.

Following mixins have to be added to your models, views and serializers:

 - `generic_permissions.models.VisibilityModelMixin`
 - `generic_permissions.views.VisibilityViewMixin`

#### Visibility classes

Visibility classes are configured as `GENERIC_PERMISSIONS_VISIBILITY_CLASSES`.

Following pre-defined classes are available:
* `generic_permissions.visibilities.Any`: Allow any user without any filtering (default)
* `generic_permissions.visibilities.Union`: Union result of a list of configured visibility classes. May only be used as base class.

To write custom visibility classes, you need to inherit from `generic_permissions.visibilities.BasePermission`.

Example:
``` python
>>> from generic_permissions.visibilities import BaseVisibility
... from tests.models import BaseModel, Model1, Model2
...
...
... class CustomVisibility(BaseVisibility):
...     @filter_queryset_for(BaseModel)
...     def filter_queryset_for_all(self, queryset, request):
...         return queryset.filter(created_by_user=request.user.username)
...
...     @filter_queryset_for(Model1)
...     def filter_queryset_for_document(self, queryset, request):
...         return queryset.exclude(category__slug='protected-category')
...
...     @filter_queryset_for(Model2)
...     def filter_queryset_for_file(self, queryset, request):
...         # Limitations for `Model1` should also be enforced on `Model2`.
...         return queryset.exclude(document__category__slug='protected-category')
```

Arguments:
* `queryset`: [Queryset](https://docs.djangoproject.com/en/3.1/ref/models/querysets/) of specific node type
* `request`: holds the [http request](https://docs.djangoproject.com/en/3.1/ref/request-response/#httprequest-objects)


## Permissions

Permission classes define who may perform which data mutation. Such can be configured as
`GENERIC_PERMISSIONS_PERMISSION_CLASSES`.

Following mixins have to be added to your models, views and serializers:

 - `generic_permissions.models.PermissionModelMixin`
 - `generic_permissions.views.PermissionViewMixin`
 - `generic_permissions.serializers.PermissionSerializerMixin`

#### Permission classes

Following pre-defined classes are available:
* `generic_permissions.permissions.AllowAny`: allow any users to perform any mutation (default)

To write custom permission classes, you need to inherit from `generic_permissions.permissions.BasePermission`.

Example:
``` python
>>> from generic_permissions.permissions import BasePermission
... from tests.models import BaseModel, Model1
...
... class CustomPermission(BasePermission):
...     @permission_for(BaseModel)
...     def has_permission_default(self, request):
...         # change default permission to False when no more specific
...         # permission is defined.
...         return False
...
...     @permission_for(Model1)
...     def has_permission_for_document(self, request):
...         return True
...
...     @object_permission_for(Model1)
...     def has_object_permission_for_document(self, request, instance):
...         return request.user.username == 'admin'
```

Arguments:
* `request`: holds the [http request](https://docs.djangoproject.com/en/3.1/ref/request-response/#httprequest-objects)
* `instance`: instance being edited by specific request
