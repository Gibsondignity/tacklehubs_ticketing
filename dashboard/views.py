from datetime import timezone
import json
from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.


@login_required()
def dashboard(request):
    
    return render(request, 'dashboard/dashboard/dashboard.html', context={})





# Events 
@login_required()
def events(request):
    form = EventForm()
    events = Event.objects.filter(user=request.user)

    #print(events)
    for event in events:
        print(event.user)
    
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
        context['picture'] = "http://localhost:8000" + event.picture.url
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
    print(events)
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
    id = request.GET.get('id')
    #print(id)
    context = {}
    try:
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
    ussd_requests = UssdRequest.objects.filter()
    
    events = Event.objects.filter(user=request.user)
    
    if request.method == "POST":
        form = UssdRequestForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Request sent successfully. We will contact you within two working days.")
            return redirect(reverse('dashboard_ussd'))
        else:
            messages.error(request, "Sorry! There was an issue requesting for USSD. Please try again later.")
    
    
    context = {'form':form, 'ussd_requests':ussd_requests, 'events':events}
    
    return render(request, 'dashboard/dashboard/ussd.html', context)




# All tickets

def ticket_reservations(request):
    
    
    tickets = Ticket.objects.all()
    
    categories = Category.objects.filter(user=request.user)
    events = Event.objects.filter(user=request.user)
    
    context = {'tickets':tickets, 'categories':categories, 'events':events}
    return render(request, 'dashboard/dashboard/tickets.html', context)



def TicketsReportById(request):
    
    if request.method == "POST":
        
        json_data = json.loads(request.body)
        from_date = json_data['from_date']
        to_date = json_data['to_date']
        companylocation = json_data['companylocation']
        sale_type = json_data['sale_type']
        user = json_data['user']
        
        sales = Ticket.objects.all()
            
        if from_date != "" and not None:
            sales = sales.filter(sales_date__date__gte=from_date)
        else: 
            sales = sales.filter(sales_date__date=timezone.now().date())
        
        if to_date != "" and not None:
            sales = sales.filter(sales_date__date__lte=to_date)
            
        if companylocation != "" and not None:
            sales = sales.filter(company_location=companylocation)
            
        if sale_type != "" and not None:
            sales = sales.filter(sale_type=sale_type)
            
        if user != "" and not None:
            sales = sales.filter(created_by=user)
             
        queryset = sales.values('id', 'sales_id', 'sales_date', 'total_amount', 'total_discount', 'net_amount', 'paid_amount', 'balance', 'cash', 'momo', 'visa', 'created_by__username', 'company_location__name', 'sale_type', 'customer')
        for data in queryset:
            if data['sale_type'] == "Credit Sale":
                #print(Sales.objects.get(id=int(data['id'])))
                data['customer'] = Ticket.objects.get(sales_id=data['sales_id']).credit_customer.name
        return JsonResponse(list(queryset), safe=False)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=400)
    
    
    
    

