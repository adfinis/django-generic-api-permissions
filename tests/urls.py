from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter()

r.register(r"test1", views.Test1ViewSet)
r.register(r"test2", views.Test2ViewSet)

urlpatterns = r.urls
