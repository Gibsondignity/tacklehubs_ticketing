# tasks.py

from datetime import datetime
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from django.http import Http404
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import render, redirect, reverse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from tickets.models import *

import urllib.request
import time


@shared_task
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
    
    
    
@shared_task   
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
    
    
    
@shared_task
def set_past_event_status():
    today = datetime.now().date()
    event = Event.objects.filter()