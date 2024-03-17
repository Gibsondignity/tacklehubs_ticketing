# tasks.py

from datetime import datetime, timedelta
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import get_object_or_404, render, redirect, reverse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils import timezone


from tickets.models import *

import urllib.request
import time


@shared_task(bind=True)
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
    try: 
        response = urllib.request.urlopen(content)
    except:
        pass
    
    
    
@shared_task(bind=True)  
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
    
    
    
@shared_task(bind=True)
def verify_payment_task(ref):
    payment = get_object_or_404(Ticket, ref=ref)
    registration_id = str(str(payment.event.event_name[0])+str(payment.catgory.category_name[0])+str(payment.event.id)+str(payment.id))
  
    verified = payment.verify_payment()
    
    if verified:
        Ticket.objects.filter(ref=ref).update(registration_id=registration_id)
        first_name = payment.name.split(" ")[0]
        send_sms(payment.phone_number, registration_id, first_name, payment.number_of_tickets)
        send_email(registration_id, first_name, payment.email, payment.number_of_tickets)
        


    
@shared_task
def verify_all_payment():
    # Get payments to verify
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    payments = Ticket.objects.filter(verify=False, date_created__gte=twenty_four_hours_ago)
    
    for payment in payments:
        registration_id = f"{payment.event.event_name[0]}{payment.category.category_name[0]}{payment.event.id}{payment.id}"
        verified = payment.verify_payment()
        if verified:
            Ticket.objects.filter(ref=payment.ref).update(registration_id=registration_id)
            first_name = payment.name.split(" ")[0]
            send_sms(payment.phone_number, registration_id, first_name, payment.number_of_tickets)
            send_email(registration_id, first_name, payment.email, payment.number_of_tickets)
        
    return "Verification process completed at " + str(timezone.now())
 
 
 
 

   
@shared_task
def set_past_event_status():
    today = datetime.now().date()
    event = Event.objects.filter()