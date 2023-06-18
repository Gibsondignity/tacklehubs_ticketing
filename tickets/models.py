from django.db import models
from accounts.models import Users

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=65)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.category_name} - {self.price}"
    
    
    
class Event(models.Model):
    event_name = models.CharField(max_length=256, )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True) 
    event_date = models.DateField()
    event_time = models.TimeField(null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.event_name


    
class Ticket(models.Model):
    name = models.CharField(max_length=65)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} -> {self.event}" 