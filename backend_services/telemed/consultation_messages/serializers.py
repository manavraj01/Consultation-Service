from rest_framework import serializers
from .models import Message
from roles.models import Role
from consultations.models import Consultation
from django.contrib.auth.models import User



class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_role_title = serializers.CharField(source='author_role.title', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'consultation',
            'author',
            'author_username',
            'author_role',
            'author_role_title',
            'content',
            'date_created',
            'last_modified',
            'archive',
        ]
        read_only_fields = [
            'date_created',
            'last_modified',
            'author_username',
            'author_role_title',
        ]

    def validate_content(self, value):
        """Ensure message content is not empty or just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value

    def validate(self, data):
        """Ensure author exists, consultation exists, author belongs to consultation, and role matches."""
        author = data.get('author')
        consultation = data.get('consultation')
        author_role = data.get('author_role')

        # Author existence check
        if not author:
            raise serializers.ValidationError({"error": "Author ID is required."})
        if not User.objects.filter(id=author.id).exists():
            raise serializers.ValidationError({"error": f"User with id {author.id} does not exist."})

        # Consultation existence check
        if not consultation:
            raise serializers.ValidationError({"error": "Consultation ID is required."})
        if not Consultation.objects.filter(id=consultation.id).exists():
            raise serializers.ValidationError({"error": f"Consultation with id {consultation.id} does not exist."})

        # Role existence check
        if not author_role:
            raise serializers.ValidationError({"error": "Author role is required."})
        if not Role.objects.filter(id=author_role.id).exists():
            raise serializers.ValidationError({"error": f"Role with id {author_role.id} does not exist."})

        # Author must belong to the consultation (patient or doctor)
        if author != consultation.patient and author != consultation.doctor:
            raise serializers.ValidationError({
                "error": "This user is not part of the consultation (neither patient nor doctor)."
            })

        # Role must match actual role in consultation
        if author == consultation.patient and author_role.title.lower() != "patient":
            raise serializers.ValidationError({
                "error": "The role must be 'patient' for the patient in this consultation."
            })
        if author == consultation.doctor and author_role.title.lower() != "doctor":
            raise serializers.ValidationError({
                "erorr": "The role must be 'doctor' for the doctor in this consultation."
            })

        return data
    

class MessageBasicSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_role_title = serializers.CharField(source='author_role.title', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'consultation',
            'author',
            'author_username',
            'author_role',
            'author_role_title',
            'content',
            'date_created',
        ]
