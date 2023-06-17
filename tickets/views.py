from django.shortcuts import render

# Create your views here.
def home(request):
    
    return render(request, 'tickets/home/home.html')






def events(request):
    
    return render(request, 'tickets/events/events.html')
