from rest_framework import serializers
from .models import Consultation
from django.db import IntegrityError

class ConsultationSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    doctor_username = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

    def validate(self, data):
        patient = data.get('patient')
        doctor = data.get('doctor')

        # Check for duplicate consultation before saving
        if Consultation.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError({
                "error": "A consultation between this patient and doctor already exists."
            })
        return data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            # Safety net: DB-level unique constraint also triggers here if race condition
            raise serializers.ValidationError({
                "error": "A consultation between this patient and doctor already exists."
            })


class ConsultationBasicSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source='patient.username', read_only=True)
    doctor_username = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id',
            'patient',
            'patient_username',
            'doctor',
            'doctor_username',
            'date_created',
            'date_modified',
            'archive'
        ]
