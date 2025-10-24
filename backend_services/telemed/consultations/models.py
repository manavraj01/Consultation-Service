from django.db import models
from django.contrib.auth.models import User
#To log events of the application
from simple_history.models import HistoricalRecords

class Consultation(models.Model):
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_consultations')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_consultations')
    #Will store the timestamp when record will be created
    date_created  = models.DateTimeField(auto_now_add=True)
    #Will modify the timestamp when it will be updated
    date_modified = models.DateTimeField(auto_now=True)

    archive = models.BooleanField(default=False, null=True, blank=True)

    #for recording history
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.updated_by

    @_history_user.setter
    def _history_user(self, value):
        self.updated_by = value

    def __str__(self):
        return f'Consultation {self.id}: {self.patient.username} & {self.doctor.username}'
    
    # Custom save method
    def save(self, *args, **kwargs):
        super(Consultation, self).save(*args, **kwargs)    

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['patient', 'doctor'], name='unique_patient_doctor_consultation')
        ]