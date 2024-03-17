from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout

from dashboard.models import *
from .backend_email import EmailBackend
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

# password reset imports
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# LOCAL IMPORTS
from .models import User

from .forms import UserForm


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from decouple import config


protocol = config("PROTOCOL")
domain = config("URL")



    
# DJANGO VIEW
def account_login(request):

    form = UserForm()
    
    context = {'form':form}
    if request.method == 'POST':
        
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        #print(email, password)
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        #print(user)
        if user != None:
            login(request, user)
            if user.is_superuser:
                messages.success(request, "You're logged in as an admin")
                return redirect(reverse("administration"))     
            else:
                bank = BankAccounts.objects.filter(user=user).first()
                userinfo = UserInfo.objects.filter(user=user).first()
                
                if not bank or not userinfo:
                    messages.success(request, "Please finish setting up your profile")
                    return redirect(reverse("profile"))
                
                messages.success(request, "Login successfull")
                return redirect(reverse("dashboard"))   
        else:
            messages.error(request, "User not found")
            return redirect("login")
    
    return render(request, "accounts/login.html", context)






def account_register(request):
    form = UserForm(request.POST or None)
    
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully")
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            error = form.errors
            print(error)
            messages.error(request, error)
            
    return render(request, "accounts/login.html", {'form': form})


 
 
 
 
def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
        
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("login"))






# reset password
def password_reset_request(request):
    #print("Here")

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            
            associated_users = User.objects.filter(Q(email=data))
            
            
            if associated_users.exists():
                    
                for user in associated_users:
                    
                    c = {
                    "email":user.email,
                    'site_name': 'Tackle Tickets',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol':  protocol,
                    'domain': domain,
                        }
                    
                    try:
                        
                        send_password(request, user.email, c)
                    
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
            else:
                messages.error(request, 'User not found')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})






def rest_email(receiver_email, context):
    
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Requested"
    message["From"] = sender_email
    message["To"] = receiver_email   
    
    html_file = "templated_email/tenant.html"
    html_content = render_to_string(html_file, 
       context = context
    )

     # Turn these into plain/html MIMEText objects
    msg = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(msg)

    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("mail.tacklehubs.com", 465) as server:
            server.login(sender_email, password)
            # print(logintest)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        pass
    





def send_password(request, email, context): 
    subject, from_email, to = 'Password Reset Requested', 'ticket@tacklehubs.com', email
    plaintext = 'Confirmation'
    #print("sending email")
    password = settings.EMAIL_HOST_PASSWORD
    sender_email = settings.EMAIL_HOST_USER

    #text_content = plaintext.render(d)
    htmly = get_template('reset_password_email.html')

    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, plaintext, from_email, [to])

    msg.attach_alternative(html_content, "text/html")

    # try:
    #     msg.send()
    # except:
    #     messages.error(request, "Email not sent")
        
    #msg.attach(msg)

    try:
        with smtplib.SMTP_SSL("mail.tacklehubs.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, email, msg.as_string()
            )
    except Exception as e:
        print(e)
        # return Response(e.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, "Email not sent")
        #pass
        
        