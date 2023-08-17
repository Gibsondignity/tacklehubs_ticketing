from django.db import models
from tickets.models import Event
from django.utils import timezone
from accounts.models import User

# Create your models here.

class UssdRequest(models.Model):
    phoneNumber = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.event.event_name
    
    
    
    
class BankAccounts(models.Model):
    account_type_choices = (('savings', 'savings'), ('current', 'current'))
    
    account_number = models.CharField(max_length=50, null=True, blank=True)
    account_name = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    account_type = models.CharField(max_length=50, null=True, blank=True, choices=account_type_choices)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, related_name='created_%(class)s_set')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=timezone.now)
    
    class Meta:
        verbose_name_plural = "Bank Accounts"
        
    def __str__(self):
        return str(self.account_number)
    
    
    
class UserInfo(models.Model):
    account_type_choices = (('savings', 'savings'), ('current', 'current'))
    
    contact_1 = models.CharField(max_length=50, null=True, blank=True)
    contact_2 = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, related_name='created_%(class)s_set')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=timezone.now)
    
    class Meta:
        verbose_name_plural = "Bank Accounts"
        
    def __str__(self):
        return str(self.account_number)