from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from .models import Room, Vote, Attendee
from .forms import RoomCodeForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = RoomCodeForm(request.POST)
        if form.is_valid():
            try:
                room = Room.objects.get(code=form.cleaned_data['room_code'])
                return render(request, 'rtemp/detail_thermometer.html', {'room':room})
            except ObjectDoesNotExist:
                form = RoomCodeForm()
                return render(request, 'rtemp/home.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomCodeForm()

    return render(request, 'rtemp/home.html', {'form': form})



def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if not Attendee.objects.filter(session=request.session.session_key) :
        a = Attendee(
            room = room,
            session = request.session.session_key,
            last_action = timezone.now()
        )
        if request.session.session_key:
            a.save()
    if room.room_type == "t":
        return render(request, 'rtemp/detail_thermometer.html', {'room':room})
    else:
        return render(request, 'rtemp/detail_needle.html', {'room':room})

def vote(request, room_id):
    room = Room.objects.get(pk=room_id)
    vote = Vote.objects.create( room = room , created_date = timezone.now())
    vote.save()
    return JsonResponse(status=200, data={'interval': room.vote_interval.total_seconds()})
