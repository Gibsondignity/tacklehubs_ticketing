
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



# Create your views here.
def home(request):
    
    
#     today = datetime.now().date()

# # Calculate the date range for the next 20 days
#     end_date = today + timedelta(days=20)
#     events = Event.objects.filter(event_date__gte = today)
        
#     upcomming_events = Event.objects.filter(event_date__range=[today, end_date]) 
    
#     media_url = "http://127.0.0.1:8000/media/"
#     context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}

    today = datetime.now().date()

    # Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today)
    
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date])
    media_url = "http://127.0.0.1:8000/media/"
    context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}
    
    
    return render(request, 'tickets/home/home.html', context)



def events(request):
    
    today = datetime.now().date()

    # Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today)
    
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date])
    media_url = "http://127.0.0.1:8000/media/"
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
    
    media_url = "http://127.0.0.1:8000/media/"
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
    payment = get_object_or_404(Ticket, ref=ref)
    registration_id = str(str(payment.event.event_name[0])+str(payment.catgory.category_name[0])+str(payment.event.id)+str(payment.id))
    print(registration_id)
  
    verified = payment.verify_payment()
    
    if verified:
        messages.success(request, "Ticket reservation was successful! Please wait while we process your sms and email.")
        Ticket.objects.filter(ref=ref).update(registration_id=registration_id)
        first_name = payment.name.split(" ")[0]
        #send_sms(payment.phone_number, registration_id, first_name, payment.number_of_tickets)
        #send_email(registration_id, first_name, payment.email, payment.number_of_tickets)
        
    
    
    return redirect('/')



# Send SMS
def send_sms(phone, id, name, number_of_tickets):
    
    phone = str(phone)
    
    try:
        if phone[0] == '+':
            phone= phone[1:].replace(' ', '')
        else:
            phone = phone.replace(' ', '')
        
        if phone[0] == '0':
            phone = '233'+phone[1:]
    except:
        pass
        
    
    message = f'''Hello%20{name}.%20Thank%20you%20for%20reserving%20your%20ticket!.%20Your%20ticket%20number%20is:%20{id}.%20Number%20of%20tickets:%20{number_of_tickets}.%20Have%20a%20great%20day!'''
    content = f"https://sms.textcus.com/api/send?apikey=PqdIBy2psAhIqkH9c5AEgRL8YcZPovcn&destination={phone}&source=ThankYou!&dlr=1&type=0&message={message}"
    print(content)
    try: 
        response = urllib.request.urlopen(content)
    except:
        pass
    
    
    
    
def send_email(id, name, email, number_of_tickets):
    
    subject = 'Ticket Reservation'


    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = email


    msg = f'Hello, {name}. Thank you for reserving your ticket. Your ticket number is: {id}. Number of tickets: {number_of_tickets} Have a great day!'
    msg = MIMEText(msg, "html")


    message.attach(msg)

    try:
        with smtplib.SMTP_SSL("mail.tacklehubs.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, email, message.as_string()
            )
    except Exception as e:
        print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        pass