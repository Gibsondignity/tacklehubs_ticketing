from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

def dashboard(request):
    
    return render(request, 'dashboard/dashboard/dashboard.html', context={})



def categories(request):
    form = CategoryForm()
    categories = Category.objects.all()
    
    if request.method == "POST":
        return
    
    
    context = {'form':form, 'categories':categories}
    return render(request, 'dashboard/dashboard/categories.html', context)



def events(request):
    form = EventForm()
    events = Event.objects.all()


    if request.method == "POST":
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect(reverse('events'))
        else:
            messages.error(request, "Event could not be created!")
    
    
    context = {'form':form, 'events':events}
    
    return render(request, 'dashboard/dashboard/events.html', context)




# def updateEvent(request):
#     if request.method != "POST":
#         messages.error(request, "Access Denied")
#     if request.method == "POST":
#         tenant_id = request.POST.get("id", None)
#         status = request.POST.get("status", None)
#         comment = request.POST.get("comment", None)
        
#         tenant = Application.objects.filter(id=tenant_id)
#         if not tenant.exists():
#             messages.error(request, "Application does not exist")
#         else:
#             tenant = tenant[0]
#             tenant.status = status
#             tenant.comment = comment
#             tenant.save()
            
#     return redirect(reverse("viewTenants"))



def getEvents(request):
    id = request.GET.get('id')
    context = {}
    try:
        event = Event.objects.get(id=int(id))
        # event = Event.objects.all().values()[int(id)]
        print(event)
        context['id'] = event.id
        context['event_name'] = event.event_name
        context['event_time'] = event.event_time
        context['description'] = event.description
        context['starting_price'] = event.starting_price
        context['location'] = event.location
        context['picture'] = event.picture.url
    except:
        messages.error(request, "There was an error fetching data!")
    print(context)
    return JsonResponse(context)
    
    
    
    
def getCategories(request):
    id = request.GET.get('id')
    context = {}
    try:
        category = Category.objects.get(id=int(id))
        print(category)
        context['id'] = category.id
        context['category_name'] = category.category_name
        context['price'] = category.price
        context['user_id'] = category.user_id
        context['date_created'] = category.date_created
    except:
        messages.error(request, "There was an error fetching data!")
    
    
    
    return JsonResponse(context)
    
    