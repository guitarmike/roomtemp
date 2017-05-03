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
                if not request.session.session_key:
                    request.session.save()
                if not room.authenticate_attendee(request.session.session_key):
                    room.add_attendee(request.session.session_key)
                return render(request, 'rtemp/detail_thermometer.html', {'room':room, 'count': room.attendee_count()})
            except ObjectDoesNotExist:
                form = RoomCodeForm()
                return render(request, 'rtemp/home.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RoomCodeForm()
    return render(request, 'rtemp/home.html', {'form': form, 'key': request.session.session_key})



def detail(request, room_id):
    if not request.session.session_key:
        request.session.save()

    room = get_object_or_404(Room, pk=room_id)
    if not room.authenticate_attendee(request.session.session_key):
        form = RoomCodeForm()
        return render(request, 'rtemp/home.html', {'form': form})
    if room.room_type == "t":
        return render(request, 'rtemp/detail_thermometer.html', {'room':room, 'count': room.attendee_count(), 'percent': room.current_vote_count()/room.attendee_count()*100})
    else:
        return render(request, 'rtemp/detail_needle.html', {'room':room})

def vote(request, room_id):
    room = Room.objects.get(pk=room_id)
    vote = Vote.objects.create( room = room , created_date = timezone.now())
    vote.save()
    percent = room.current_vote_count()/room.attendee_count()*100
    return JsonResponse(status=200, data={
        'interval': room.vote_interval.total_seconds()
    })

def status(request, room_id):
    room = Room.objects.get(pk=room_id)
    votes = room.current_vote_count()
    attendees = room.attendee_count()
    percent = "{:.2f}".format(votes/attendees*100)
    return JsonResponse(status=200, data={
        'votes': votes,
        'attendees': attendees,
        'percent': percent
    })
