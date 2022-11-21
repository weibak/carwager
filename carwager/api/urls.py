# api/urls.py

from django.urls import include, path
from rest_framework import routers
from api.showbill.views import AdvertViewSet
from api.users.views import UserCreateView, UserLoginView, UserLogoutView, UserViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"adverts", AdvertViewSet, basename="adverts")
router.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
