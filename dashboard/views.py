from django.shortcuts import render

# Create your views here.

def dashboard(request):
    
    return render(request, 'dashboard/dashboard/dashboard.html', context={})



def categories(request):
    
    return render(request, 'dashboard/dashboard/categories.html', context={})



def events(request):
    
    return render(request, 'dashboard/dashboard/events.html', context={})



