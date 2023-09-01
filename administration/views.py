from datetime import timezone
import json
from django.shortcuts import render, redirect, reverse
from dashboard.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
# Create your views here.


@login_required()
def admin_dashboard(request):

        
    return render(request, 'administration/dashboard.html', context={})





# Events 
@login_required()
def admin_events(request):
    events = Event.objects.all()

    context = {'events':events}
    
    return render(request, 'administration/events.html', context)








@login_required()
def admin_updateEvent(request):
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
def admin_deleteEvents(request):
    
    id = request.POST.get('id')
    event = Event.objects.filter(id=int(id)).first()
    try:
        event.delete() 
        messages.success(request, "Event deleted successfully!")
    except event.DoesNotExist():
        messages.error(request, "There was an error deleteing this event!")
    
    return redirect(reverse("dashboard_event"))







@login_required()
def admin_getEvents(request):
    id = request.GET.get('id')
    context = {}
    try:
        event = Event.objects.get(id=int(id))
       
        context['id'] = event.id
        context['event_name'] = event.event_name
        context['event_date'] = event.event_date
        context['event_time'] = event.event_time
        context['description'] = event.description
        context['starting_price'] = event.starting_price
        context['location'] = event.location
        if settings.DEBUG == True:
            context['picture'] = "http://localhost:8000" + event.picture.url
        else:
            context['picture'] = "https://tackletickets.org" + event.picture.url
    except:
        messages.error(request, "There was an error fetching data!")
        
    #print(context)
    return JsonResponse(context)
    
    
    
  
  
  
# Categories
@login_required()
def admin_categories(request):
    form = CategoryForm()
    categories = Category.objects.all()
    
    events = Event.objects.all()
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
    
    return render(request, 'administration/categories.html', context)







@login_required()
def admin_updateCategory(request):
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
def admin_deleteCategory(request):
    
    id = request.POST.get('id')
    category = Category.objects.filter(id=int(id)).first()
    try:
        category.delete() 
        messages.success(request, "category deleted successfully!")
    except category.DoesNotExist():
        messages.error(request, "There was an error deleteing this category!")
    
    return redirect(reverse("categories"))





@login_required() 
def admin_getCategories(request):
    
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
def admin_ussd(request):
    form = UssdRequestForm()
    ussd_requests = UssdRequest.objects.all()
    
    events = Event.objects.all()
    
    if request.method == "POST":
        form = UssdRequestForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Request sent successfully. We will contact you within two working days.")
            return redirect(reverse('dashboard_ussd'))
        else:
            messages.error(request, "Sorry! There was an issue requesting for USSD. Please try again later.")
    
    
    context = {'form':form, 'ussd_requests':ussd_requests, 'events':events}
    
    return render(request, 'administration/ussd.html', context)





@login_required()
def admin_profile(request):
    
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
    return render(request, 'administration/profile.html', context)




@login_required()
def admin_UserInformation(request):

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
def admin_ticket_reservations(request):
    
    
    tickets = Ticket.objects.all()
    categories = Category.objects.all()
    events = Event.objects.all()
    
    context = {'tickets':tickets, 'categories':categories, 'events':events}
    return render(request, 'administration/tickets.html', context)


@login_required()
def admin_TicketsReportById(request):
    
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
    
    
    
