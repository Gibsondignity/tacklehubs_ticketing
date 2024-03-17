
from datetime import datetime, timedelta
from .models import *
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.conf import settings
import json
import urllib.request
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import decimal
from dashboard.task import send_email, send_sms, verify_payment_task
from decouple import config


url = config('URL')


# Create your views here.
def home(request):
    

    today = datetime.now().date()

    # Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today, status="Approved").order_by('-date_created')[:12]
    
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date])
    
    media_url = f"http://{url}/media/" 
    
    context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}
    
    return render(request, 'tickets/home/home.html', context)





def events(request):
    
    today = datetime.now().date()

    # Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today, status="Approved")
    
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date])
    
    media_url = f"http://{url}/media/" 
        
    context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}
    
    return render(request, 'tickets/events/events.html', context)






def event(request, id, slug):
    
    if request.method == "POST":
        number_of_tickets = request.POST.get('number_of_tickets')
        category_id = request.POST.get('category_id')
        price = request.POST.get('price')
        event_id = request.POST.get('event_id')
        context = {
            'number_of_tickets':number_of_tickets,
            'category_id':category_id,
            'price':price,
            'event_id':event_id,
            }
        #print(context)
        return render(request, 'payment/initiate_payment.html', context)
    
    
    event = Event.objects.filter(id=id).first()
    categories = Category.objects.filter(event=event)
    
    media_url = f"http://{url}/media/"  
        
    print("It worked", categories)
    context = {"event": event, "media_url":media_url, 'categories':categories}
    
    return render(request, 'tickets/event/event.html', context)


    
    

def initiate_payment(request):

    if request.method == "POST":
        payment = Ticket()
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('phone_number')
        number_of_tickets = request.POST.get('number_of_tickets')
        category_id = request.POST.get('category_id')
        price = request.POST.get('price')
        event_id = request.POST.get('event_id')
        
        context = {
            'number_of_tickets':number_of_tickets,
            'category_id':category_id,
            'price':price,
            'event_id':event_id,
            }
        
        event_id = Event.objects.filter(id=int(event_id)).first()
        category_id = Category.objects.filter(id=int(category_id)).first()
        
        amount = float(price) * int(number_of_tickets)
        payment.name = name
        payment.email = email
        payment.phone_number = contact
        payment.amount = amount
        payment.number_of_tickets = number_of_tickets
        payment.event = event_id
        payment.catgory = category_id
        
        payment.save()
        
        context = {"pub_key":settings.PAYSTACK_PUBLIC_KEY, 'payment':payment, 'amount':amount}
        return render(request, 'payment/make_payment.html', context)

    return render(request, 'payment/initiate_payment.html')






def verify_payment(request, ref: str) -> HttpResponse:
    messages.success(request, 'Thank you for for your ticket reservation. Please wait while we process your ticket.')
    verify_payment_task().delay(ref) # Calling the function as
        
    return redirect('/')



# Send SMS
