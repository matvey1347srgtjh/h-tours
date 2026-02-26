from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required

def event_list(request):
    events = Event.objects.all().order_by('event_datetime')
    return render(request, 'list.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            from django.contrib.auth.models import User
            event.user = User.objects.first() or User.objects.create(username='admin')
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'form.html', {'form': form})