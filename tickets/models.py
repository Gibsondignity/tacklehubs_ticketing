from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import secrets
from .paystack import PayStack

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
    status_choices = (('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'))
    event_name = models.CharField(max_length=256, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    event_date = models.DateField()
    event_time = models.TimeField(null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    picture = FileField(upload_to='gallery', blank=True, null=True)
    location = models.CharField(max_length=65, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    status = models.CharField(default="Pending", choices=status_choices, max_length=25)
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
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_tickets = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    catgory = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    sessionID = models.CharField(max_length=65, null=True, blank=True)
    level = models.IntegerField(null=True , default=0)
    otp = models.CharField(max_length=50,null=True ,blank=True)
    ref = models.CharField(max_length=50,blank=True,null=True)
    registration_id = models.CharField(max_length=50,blank=True,null=True)
    verify = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}  {self.contact}  {self.verified} '
    
    
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'Payment: {self.amount}' 

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(10)
            object_with_similar_ref = Ticket.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)
   
    
    def verify_payment(self):
        Paybox = PayStack()
        status, result = Paybox.verify_payment(self.ref)
        if status:
            print(result['amount'])
            if result['amount'] == self.amount*100:
                self.verify = True
            self.save()

        if self.verify:
            return True
        return False
    
    
    
    