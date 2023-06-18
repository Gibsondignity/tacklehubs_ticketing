from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    
    return render(request, 'tickets/home/home.html')



def events(request):
    
    events = Event.objects.all()
    media_url = "http://127.0.0.1:8000/media/"
    context = {"events": events, "media_url":media_url}
    return render(request, 'tickets/events/events.html', context)
