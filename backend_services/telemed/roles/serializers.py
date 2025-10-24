from rest_framework import serializers
from .models import Role
from django.db import IntegrityError

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

    def validate_title(self, value):
        # Check if role with same title already exists (case-insensitive)
        if Role.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError("A role with this title already exists.")
        return value

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "error": "A role with this title already exists."
            })


class RoleBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'title'
        ]