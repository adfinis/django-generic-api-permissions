from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter()

r.register(r"test1", views.Dummy1ViewSet)
r.register(r"test2", views.Dummy2ViewSet)

urlpatterns = r.urls
