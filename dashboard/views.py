from django.shortcuts import render, redirect, reverse
from .forms import *
from django.contrib import messages

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



