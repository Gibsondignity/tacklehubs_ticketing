# tasks.py

from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail

import email
from urllib import request
from .models import Account
from accounts.models import Users
from django.http import Http404
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import render, redirect, reverse


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@shared_task
def your_task():
    # Your task logic here
    result = perform_task()
    
    # After task completion, send email and SMS notification
    send_email_notification.delay()
    send_sms_notification.delay()

@shared_task
def send_email_notification():
    # Send email notification
    send_mail('Task Completed', 'Your task has been completed successfully.', 'from@example.com', ['to@example.com'])

@shared_task
def send_sms_notification():
    # Send SMS notification using Twilio or any other service
    client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
    message = client.messages.create(body="Your task has been completed successfully.", from_="YOUR_TWILIO_NUMBER", to="RECIPIENT_NUMBER")




    
def book_email(receiver_email, first_name, contact, date, book_status):
    
    sender_email = "election@cemswiss.com"
    # receiver_email = "gibsondignty@gmail.com"
    password = "Gibson@2022" 

    message = MIMEMultipart("alternative")
    message["Subject"] = "EasyRent Ghana Appartment Viewing"
    message["From"] = sender_email
    message["To"] = receiver_email   
    
    html_file = "templated_email/book.html"
    html_content = render_to_string(html_file, 
       context={
            'name': first_name,
            'email':receiver_email,
            'contact':contact,
            'date': date,
            'book_status': book_status
        },    
    )

     # Turn these into plain/html MIMEText objects
    msg = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(msg)

    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("mail.cemswiss.com", 465) as server:
            server.login(sender_email, password)
            # print(logintest)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # print(e)
        pass
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
def tenant_email(receiver_email, first_name, tenant_status):
    
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    
    if tenant_status == "registered":
        subject = "EasyRent Account Registration"
    elif tenant_status == "Approved":
        subject = "Your Account has been Approved"
    elif tenant_status == "renewal":
        subject = "Your application has been Successfully Renewed"
    else:
        subject = "EasyRent Ghana"
    
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email   
    
    html_file = "templated_email/tenant.html"
    html_content = render_to_string(html_file, 
       context={
            'name': first_name,
            'email':receiver_email,
            'tenant_status': tenant_status
        },    
    )

     # Turn these into plain/html MIMEText objects
    msg = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(msg)

    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("mail.easyrentgh.com", 465) as server:
            server.login(sender_email, password)
            # print(logintest)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        pass
    
    

def application_status_email(receiver_email, first_name, tenant_status, comment, status):
    
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "EasyRent Application Status"
    message["From"] = sender_email
    message["To"] = receiver_email   
    
    html_file = "templated_email/tenant.html"
    html_content = render_to_string(html_file, 
       context={
            'name': first_name,
            'email':receiver_email,
            'tenant_status': tenant_status,
            'comment': comment,
            'status': status
        },    
    )

     # Turn these into plain/html MIMEText objects
    msg = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(msg)

    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("mail.easyrentgh.com", 465) as server:
            server.login(sender_email, password)
            # print(logintest)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        pass
    
    


# admin email
def admin_email(admin_status, name, typeOfRoom, preferedLocation, budgetedMonthlyRent):
    
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = "gibsondignty@gmail.com"
    
    if admin_status == "new":
        subject = "Renter Seeking an Apartment"
    
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    
    html_file = "templated_email/admin.html"
    html_content = render_to_string(html_file, 
       context={
            'email': receiver_email,
            'admin_status': admin_status,
            'name': name,
            'typeOfRoom': typeOfRoom,
            'preferedLocation': preferedLocation,
            'budgetedMonthlyRent': budgetedMonthlyRent, 
        },    
    )

     # Turn these into plain/html MIMEText objects
    msg = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(msg)

    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("mail.easyrentgh.com", 465) as server:
            server.login(sender_email, password)
            # print(logintest)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        pass
    
    
    

