from django.db import models
#To log events of the application
from simple_history.models import HistoricalRecords

class Role(models.Model):
    title = models.CharField(max_length = 100)
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
        return self.title
    
    # Custom save method
    def save(self, *args, **kwargs):
        super(Role, self).save(*args, **kwargs)    

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_role_title')
        ]