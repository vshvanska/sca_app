from django.urls import path, include
from rest_framework import routers

from cats.views import CatViewSet

router = routers.DefaultRouter()
router.register("", CatViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "cats"
