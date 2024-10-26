from rest_framework import serializers

from missions.models import Target, Mission


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "is_completed")
        read_only_fields = ("id",)


class TargetRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "name", "country", "notes", "is_completed", "mission")


class TargetUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        if instance.is_completed or instance.mission.is_completed:
            raise serializers.ValidationError("Completed targets cannot be updated")
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Target
        fields = ("notes", "is_completed")


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    class Meta:
        model = Mission
        fields = ("id", "cat", "is_completed", "targets")
        read_only_fields = ("id", "is_completed")


class MissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ("cat",)
