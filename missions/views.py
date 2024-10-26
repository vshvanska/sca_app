from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from missions.models import Mission, Target
from missions.serializers import (
    MissionSerializer,
    MissionUpdateSerializer,
    TargetRetrieveSerializer,
    TargetUpdateSerializer,
)


class MissionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):

    serializer_class = MissionSerializer
    queryset = Mission.objects.all()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return MissionUpdateSerializer
        return MissionSerializer


class TargetsViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):

    serializer_class = TargetRetrieveSerializer
    queryset = Target.objects.all()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return TargetUpdateSerializer
        return TargetRetrieveSerializer
