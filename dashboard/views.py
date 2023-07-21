from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

def dashboard(request):
    
    return render(request, 'dashboard/dashboard/dashboard.html', context={})





# Events 

def events(request):
    form = EventForm()
    events = Event.objects.all()


    if request.method == "POST":
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect(reverse('dashboard_events'))
        else:
            messages.error(request, "Event could not be created!")
    
    
    context = {'form':form, 'events':events}
    
    return render(request, 'dashboard/dashboard/events.html', context)




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
              

    return redirect(reverse("dashboard_event"))





def deleteEvents(request):
    
    id = request.POST.get('id')
    event = Event.objects.filter(id=int(id)).first()
    try:
        event.delete() 
        messages.success(request, "Event deleted successfully!")
    except event.DoesNotExist():
        messages.error(request, "There was an error deleteing this event!")
    
    return redirect(reverse("categories"))



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

def categories(request):
    form = CategoryForm()
    categories = Category.objects.all()
    
    events = Event.objects.all()
    
    if request.method == "POST":
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect(reverse('categories'))
        else:
            messages.error(request, "Event could not be created!")
    
    
    context = {'form':form, 'categories':categories, 'events':events}
    
    return render(request, 'dashboard/dashboard/categories.html', context)



def updateCategory(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    if request.method == "POST":
        id = request.POST.get("id", None) 
        event = Event.objects.filter(id=int(id)).first()
        print(event)
        form = CategoryForm(request.POST or None, instance=event)
        #print(form)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Category updated succcessfully!")
        else :
            messages.error(request, "Category updated successfully!")
              

    return redirect(reverse("categories"))






def deleteCategory(request):
    
    id = request.POST.get('id')
    category = Category.objects.filter(id=int(id)).first()
    try:
        category.delete() 
        messages.success(request, "category deleted successfully!")
    except category.DoesNotExist():
        messages.error(request, "There was an error deleteing this category!")
    
    return redirect(reverse("categories"))

  
def getCategories(request):
    id = request.GET.get('id')
    print(id)
    context = {}
    try:
        category = Category.objects.get(id=int(id))
        context['id'] = category.id
        context['category_name'] = category.category_name
        context['price'] = category.price
        if category.event:
            context['event'] = category.event.id
        print(context)
        
    except:
        messages.error(request, "There was an error fetching data!")
    
    #print(context)
    
    return JsonResponse(context)
    
    