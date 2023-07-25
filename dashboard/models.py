from django.db import models
from tickets.models import Event

# Create your models here.

class UssdRequest(models.Model):
    phoneNumber = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.event.event_name