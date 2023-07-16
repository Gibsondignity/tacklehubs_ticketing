from django.shortcuts import render
from .forms import *
from django.contrib import messages

# Create your views here.

def dashboard(request):
    
    return render(request, 'dashboard/dashboard/dashboard.html', context={})



def categories(request):
    form = CategoryForm()
    
    
    if request.method == "POST":
        return
    
    
    context = {'form':form}
    return render(request, 'dashboard/dashboard/categories.html', context)



def events(request):
    form = EventForm()
    
    messages.success(request, "Successfully reloaded page")


    if request.method == "POST":
        form = EventForm(request.POST or None, request.FILES or None)
        
        print("form")
    
    
    context = {'form':form}
    
    return render(request, 'dashboard/dashboard/events.html', context)



