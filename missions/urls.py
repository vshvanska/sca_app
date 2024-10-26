from django.urls import path, include
from rest_framework import routers
from missions.views import MissionViewSet, TargetsViewSet

router = routers.DefaultRouter()
router.register("", MissionViewSet)
router.register(r"targets", TargetsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "missions"
