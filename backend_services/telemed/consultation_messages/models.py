from django.db import models
from django.contrib.auth.models import User
from consultations.models import Consultation
from simple_history.models import HistoricalRecords
from roles.models import Role  

class Message(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    archive = models.BooleanField(default=False, null=True, blank=True)


    history = HistoricalRecords()

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f'Message by {self.author.username} at {self.date_created}'

    #for recording history
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.updated_by

    @_history_user.setter
    def _history_user(self, value):
        self.updated_by = value

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)    