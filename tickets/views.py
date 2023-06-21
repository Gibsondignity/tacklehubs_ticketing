from django.shortcuts import render
from datetime import datetime, timedelta
from .models import *

# Create your views here.
def home(request):
    
    
    today = datetime.now().date()

# Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today)
        
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date]) 
    
    media_url = "http://127.0.0.1:8000/media/"
    context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}
    
    return render(request, 'tickets/home/home.html', context)



def events(request):
    
    today = datetime.now().date()

    # Calculate the date range for the next 20 days
    end_date = today + timedelta(days=20)
    events = Event.objects.filter(event_date__gte = today)
    
    upcomming_events = Event.objects.filter(event_date__range=[today, end_date])
    media_url = "http://127.0.0.1:8000/media/"
    context = {"events": events, "media_url":media_url, 'upcomming_events':upcomming_events}
    
    return render(request, 'tickets/events/events.html', context)






def event(request, id, slug):
    
    event = Event.objects.filter(id=id).first()
    categories = Category.objects.filter(event=event)
    
    media_url = "http://127.0.0.1:8000/media/"
    print("It worked", categories)
    context = {"event": event, "media_url":media_url, 'categories':categories}
    
    return render(request, 'tickets/event/event.html', context)
