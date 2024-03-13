# tasks.py

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

import urllib.request
import time


@shared_task
# Send SMS
def send_sms_with_celery(phone, name):
    
    phone = str(phone)
    
    try:
        if phone[0] == '+':
            phone= phone[1:].replace(' ', '')
        else:
            phone = phone.replace(' ', '')
    except:
        pass
        
    
    message = f'''Hello%20{name}.%20Thank%20you%20for%20submitting%20your%20application!%20We%20have%20received%20it%20and%20will%20review%20it%20carefully.%20You%20will%20hear%20from%20us%20soon%20regarding%20the%20next%20steps.%20Your%20Application%20ID%20is:%20.%20Have%20a%20great%20day!'''
    content = f"https://sms.textcus.com/api/send?apikey=Zu6MKbqA5DaL5awJPl0Nxa8bvYbDFeuT&destination={phone}&source=NiBS&dlr=1&type=0&message={message}"
    #print(content)
    #response = urllib.request.urlopen("https://sms.textcus.com/api/send?apikey=Zu6MKbqA5DaL5awJPl0Nxa8bvYbDFeuT&destination=233245534524&source=NiBS&dlr=1&type=0&message=%20Thank%20you%20for%20completing%20your%20Application%20with%20Nobel%20International%20Business%20School.%20Your%20Application%20ID%20is:%20NIBS21024.%20This%20email%20confirms%20that%20your%20application%20has%20been%20received.%20We%20will%20review%20it%20and%20get%20back%20to%20you%20as%20soon%20as%20possible.%20In%20the%20meantime,%20if%20you%20have%20any%20questions,%20email%20us%20at%20apply@nibs.edu.gh,%20and%20we%27ll%20be%20happy%20to%20help%20you.%20Sincerely,%20Nobel%20International%20Business%20School.%20NiBS%20Admissions%20Team.").read()
    try:
        urllib.request.urlopen(content)
    except:
        pass
    
    
  
  
@shared_task
def send_email_with_celery(email, message, subject):
    
    sender_email = settings.EMAIL_HOST_USER
    to = email
    
    # Send email using Django's send_mail function
    send_mail(
        subject,
        message,
        sender_email,
        [to],
        fail_silently=False,
    )
    
    
    # d = { 'name': name, 'application_id': application_id, 'application_status':application_status }
    
    # #text_content = plaintext.render(d)
    # htmly = get_template('new_email.html')
    
    # html_content = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])
    
    # msg.attach_alternative(html_content, "text/html")
    
    # try:
    #     msg.send()
    # except:
    #     pass