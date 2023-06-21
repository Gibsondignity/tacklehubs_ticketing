from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.
class FileField(models.FileField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", 1024*1024)
        super().__init__(*args, **kwargs)
        
    def upload_to(self, instance, filename):
        file = instance.file
        if file.size > self.max_upload_size:
            raise ValidationError("File size must be less than 1 MB")
        


class Event(models.Model):
    event_name = models.CharField(max_length=256, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    event_date = models.DateField()
    event_time = models.TimeField(null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    picture = FileField(upload_to='gallery', blank=True, null=True)
    location = models.CharField(max_length=65, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.event_name)  # Generate slug from event name
        super(Event, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.event_name
    
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=65)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.category_name} - {self.price}"
    
    
    



    
class Ticket(models.Model):
    name = models.CharField(max_length=65)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    #event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    catgory = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} -> {self.event}" 
    
    
    
    