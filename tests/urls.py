from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter()

r.register(r"test", views.TestViewSet)

urlpatterns = r.urls
