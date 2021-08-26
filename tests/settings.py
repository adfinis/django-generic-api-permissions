DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
}

INSTALLED_APPS = (
    "tests",
    "generic_permissions.apps.GenericPermissionsConfig",
)

GENERIC_PERMISSIONS_PERMISSION_CLASSES = ["generic_permissions.permissions.AllowAny"]
GENERIC_PERMISSIONS_VISIBILITY_CLASSES = ["generic_permissions.visibilities.Any"]
GENERIC_PERMISSIONS_VALIDATION_CLASSES = ["generic_permissions.validations.PassThrough"]

ROOT_URLCONF = "tests.urls"

SECRET_KEY = "foobar"
USE_TZ = True
