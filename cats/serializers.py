import requests
from rest_framework import serializers

from cats.models import Cat
from spa.settings import CAT_BREEDS_URL


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = "__all__"

    def validate_breed(self, breed):
        breeds_response = requests.get(CAT_BREEDS_URL)
        if breeds_response.status_code != 200:
            raise serializers.ValidationError(
                "Creating cats is unavailable right now. Try later."
            )
        breeds = breeds_response.json()

        validated_breed = None

        for valid_breed in breeds:
            if valid_breed["name"] == breed:
                validated_breed = breed
                break

        if not validated_breed:
            raise serializers.ValidationError("Invalid breed")
        return breed


class CatUpdateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        unsupported_fields = set(self.initial_data.keys()) - set(self.fields)
        if unsupported_fields:
            raise serializers.ValidationError(
                f"Fields {unsupported_fields} are not allowed for update."
            )
        return attrs

    class Meta:
        model = Cat
        fields = ["salary", "years_of_experience"]
