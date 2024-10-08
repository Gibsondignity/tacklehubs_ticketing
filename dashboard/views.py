from datetime import timezone
import json
from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import *
# Create your views here.

from decouple import config


domain = config('URL')
protocol = config('PROTOCOL')


@login_required()
def dashboard(request):
 
    total_events = Event.objects.filter( user=request.user).count()
    events = Event.objects.filter( user=request.user)
    total_categories = Category.objects.filter( user=request.user).count()
    total_ussd_requests = UssdRequest.objects.filter(user=request.user).count()
    total_ussd_request = UssdRequest.objects.filter(user=request.user)
    total_tickets = 0
    paid_tickets = 0
    unpaid_tickets = 0
    total_number_of_tickets = 0
    
    for event in events:
        if event.user == request.user:
            new_events = event.ticket_set.all()
            for new_event in new_events:
                total_tickets += new_event.amount
                if new_event.verify == True:
                    paid_tickets+=new_event.amount
                    total_number_of_tickets+=1
                if new_event.verify == False:
                    unpaid_tickets+=new_event.amount
            
    
    context = {'total_events':total_events, 
               'total_categories':total_categories, 
               'total_ussd_requests': total_ussd_requests, 
               'total_ussd_request': total_ussd_request,
               'total_tickets': total_tickets,
               'paid_tickets': paid_tickets,
               'unpaid_tickets': unpaid_tickets,
               'total_number_of_tickets': total_number_of_tickets,
               'domain':domain,
               'protocol':protocol,
               }
    return render(request, 'dashboard/dashboard/dashboard.html', context)





# Events 
@login_required()
def events(request):
    form = EventForm()
    events = Event.objects.filter(user=request.user)

    #print(events)
    
    if request.method == "POST":
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.user = request.user
            
            user.save()
            
            messages.success(request, "Event created successfully!")
            return redirect(reverse('dashboard_events'))
        else:
            messages.error(request, "Event could not be created!")
    
    
    context = {'form':form, 'events':events}
    
    return render(request, 'dashboard/dashboard/events.html', context)





@login_required
def view_event_tickets(request, slug, id):
    event = Event.objects.filter(id=id).first()
    tickets = event.ticket_set.all()
    total_verified = tickets.filter(verify=True).count()
    total_unverified = tickets.filter(verify=False).count()
    total_amount_of_tickets = 0
    for ticket in tickets:
        if ticket.verify == True:
            total_amount_of_tickets += ticket.amount
        
    context = {
               'event': event, 
               'tickets': tickets, 
               'total_verified': total_verified, 
               'total_unverified': total_unverified,
               'total_amount_of_tickets': total_amount_of_tickets,
               }
    
    return render(request, 'dashboard/dashboard/event_details.html', context)






@login_required()
def updateEvent(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    if request.method == "POST":
        id = request.POST.get("id", None) 
        #print(id)
        image = request.FILES.get('picture') 
        event = Event.objects.filter(id=int(id)).first()
        form = EventForm(request.POST or None, request.FILES or None, instance=event)
        
        if form.is_valid():
            form.save(commit=False)
            if image:
                form.picture = image
                
            form.save()   
            messages.success(request, "Event updated succcessfully")
        else :
            messages.error(request, "There was an error updating event")
              

    return redirect(reverse("dashboard_events"))






@login_required()
def deleteEvents(request):
    
    id = request.POST.get('id')
    event = Event.objects.filter(id=int(id)).first()
    try:
        event.delete() 
        messages.success(request, "Event deleted successfully!")
    except event.DoesNotExist():
        messages.error(request, "There was an error deleteing this event!")
    
    return redirect(reverse("dashboard_event"))







@login_required()
def getEvents(request):
    id = request.GET.get('id')
    context = {}
    try:
        event = Event.objects.get(id=int(id))
        # event = Event.objects.all().values()[int(id)]
        #print(event)
        context['id'] = event.id
        context['event_name'] = event.event_name
        context['event_date'] = event.event_date
        context['event_time'] = event.event_time
        context['description'] = event.description
        context['starting_price'] = event.starting_price
        context['location'] = event.location

        context['picture'] = f"{protocol}://{domain}" + event.picture.url

    except:
        messages.error(request, "There was an error fetching data!")
        
    #print(context)
    return JsonResponse(context)
    
    
    
  
  
  
# Categories
@login_required()
def categories(request):
    form = CategoryForm()
    categories = Category.objects.filter(user=request.user)
    
    events = Event.objects.filter(user=request.user)
    #print(events)
    if request.method == "POST":
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            messages.success(request, "Event created successfully!")
            return redirect(reverse('categories'))
        else:
            messages.error(request, "Event could not be created!")
    
    
    context = {'form':form, 'categories':categories, 'events':events}
    
    return render(request, 'dashboard/dashboard/categories.html', context)







@login_required()
def updateCategory(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    if request.method == "POST":
        id = request.POST.get("id", None) 
        category = Category.objects.filter(id=int(id)).first()
        #print(category)
        form = CategoryForm(request.POST or None, instance=category)
        #print(form)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Category updated succcessfully!")
        else :
            messages.error(request, "Category updated successfully!")
              

    return redirect(reverse("categories"))





@login_required()
def deleteCategory(request):
    
    id = request.POST.get('id')
    category = Category.objects.filter(id=int(id)).first()
    try:
        category.delete() 
        messages.success(request, "category deleted successfully!")
    except category.DoesNotExist():
        messages.error(request, "There was an error deleteing this category!")
    
    return redirect(reverse("categories"))





@login_required() 
def getCategories(request):
    
    context = {}
    try:
        id = request.GET.get('id')
        category = Category.objects.get(id=int(id))
        context['id'] = category.id
        context['category_name'] = category.category_name
        context['price'] = category.price
        if category.event:
            context['event'] = category.event.id
        #print(context)
        
    except:
        messages.error(request, "There was an error fetching data!")
    
    #print(context)
    
    return JsonResponse(context)





@login_required()
def ussd(request):
    form = UssdRequestForm()
    ussd_requests = UssdRequest.objects.filter(user=request.user)
    
    
    events = Event.objects.filter(user=request.user)
    
    if request.method == "POST":
        form = UssdRequestForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            messages.success(request, "Request sent successfully. We will contact you within two working days.")
            return redirect(reverse('dashboard_ussd'))
        else:
            messages.error(request, "Sorry! There was an issue requesting for USSD. Please try again later.")
    
    
    context = {'form':form, 'ussd_requests':ussd_requests, 'events':events}
    
    return render(request, 'dashboard/dashboard/ussd.html', context)





@login_required()
def profile(request):
    
    user = request.user
    user_bank_details = BankAccounts.objects.filter(user=user).first()

    user_info = UserInfo.objects.filter(user=user).first()

    if user_info:
        user_form = UserInfoForm(instance=user_info)
    else:
        user_form = UserInfoForm()
    
    if user_bank_details:
        form = BankAccountsForm(instance=user_bank_details)
    else:
        form = BankAccountsForm()
        
    if request.method == "POST":
        if user_bank_details:
            form = BankAccountsForm(request.POST or None, instance=user_bank_details)
            if form.is_valid():
                form.save()
                messages.success(request, "Bank account info updated succesfully!")
        else:
            form = BankAccountsForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                user.user = request.user
                user.save()
                messages.success(request, "Bank account info created succesfully!")
    context = {'form': form, 'user_form':user_form} 
    return render(request, 'dashboard/dashboard/profile.html', context)




@login_required()
def UserInformation(request):

    user = request.user
    user_info = UserInfo.objects.filter(user=user).first()
        
    if request.method == "POST":
        if user_info:
            form = UserInfoForm(request.POST or None, instance=user_info)
            if form.is_valid():
                form.save()
                messages.success(request, "User info updated succesfully!")
        else:
            form = UserInfoForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                user.user = request.user
                user.save()
                messages.success(request, "User info created succesfully!")

    return redirect(reverse('profile'))
    

# All tickets
@login_required()
def ticket_reservations(request):
    
    
    tickets = Ticket.objects.all()
    categories = Category.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user)
    
    context = {'tickets':tickets, 'categories':categories, 'events':events}
    return render(request, 'dashboard/dashboard/tickets.html', context)


@login_required()
def TicketsReportById(request):
    
    if request.method == "POST":  
        json_data = json.loads(request.body)
        from_date = json_data['from_date']
        to_date = json_data['to_date']
        event_id = json_data['event_id']
        payment = json_data['payment']
        category = json_data['category']
        event = json_data['event']

        ticket = Ticket.objects.all()
        
        if payment == 'verified':
             payment = True
        elif payment == "not_verified":
            payment = False


        if event or category:
            
            if event != "" and not None:
                ticket = ticket.filter(event=event)
                
            if category != "" and not None:
                ticket = ticket.filter(catgory=category)
   
            if from_date != "" and not None:
                ticket = ticket.filter(date_created__gte=from_date)
            else: 
                ticket = ticket.filter(date_created__date=timezone.now().date())
            
            if to_date != "" and not None:
                ticket = ticket.filter(date_created__date__lte=to_date)
            else:
                ticket = ticket.filter(date_created__date=timezone.now().date())
                
            if event_id != "" and not None:
                ticket = ticket.filter(registration_id=event_id)
                
            if payment != "" and not None:
                ticket = ticket.filter(verify=payment)
                
        else:
            ticket = []
            return JsonResponse(ticket, safe=False)
            
              
        queryset = ticket.values('id', 'name', 'email', 'phone_number', 'amount', 'number_of_tickets', 'registration_id', 'verify', 'date_created')
        #print(queryset)
        return JsonResponse(list(queryset), safe=False)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=400)
    
    
    
    

