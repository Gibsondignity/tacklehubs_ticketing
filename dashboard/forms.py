from tickets.models import *
from .models import *
from django import forms
from django.forms import ModelForm



class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = (
            'category_name',
            'price',
            'event',
                )
        
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
        
        
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = (
            'event_name',
            'event_date',
            'event_time',
            'description',
            'starting_price',
            'picture',
            'location',
                )
        
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'True', 'type':'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'required': 'True', 'type':'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'True' }),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'True'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'required':'True', 'accept':"image/*"}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }
        
        
    
    
        
class BankAccountsForm(ModelForm):
    class Meta:
        model = BankAccounts
        fields = (
            'account_number',
            'account_name',
            'bank_name',
            'account_type',
            'bank_branch',
                )
        
        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'account_type': forms.Select(attrs={'class': 'form-control', 'required': 'True' }),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }
        
        
class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = (
            'contact_1',
            'contact_2',
            'location',
            'zip_code',
                )
        
        widgets = {
            'contact_1': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'contact_2': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }
        
        
        
        
class UssdRequestForm(ModelForm):
    class Meta:
        model = UssdRequest
        fields = (
            'phoneNumber',
            'event',
                )
        
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'event': forms.Select(attrs={'class': 'form-control'}),
        }