from django.shortcuts import render, get_object_or_404, redirect
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
                return redirect(room)
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
        return render(request, 'rtemp/detail_thermometer.html', {'room':room, 'show_widget':room.show_widget(request.user), 'count': room.attendee_count(), 'percent': room.current_vote_count()/room.attendee_count()*100})
    else:
        return render(request, 'rtemp/detail_needle.html', {'room':room, 'show_widget':room.show_widget(request.user), 'count':room.attendee_count(), 'percent': room.current_vote_count()/room.attendee_count()*100})

def vote(request, room_id):
    room = Room.objects.get(pk=room_id)
    # Need error checking to prevent vote from being cast with improper payload for room type
    if room.room_type == "n":
        if request.GET.get('payload'):
            thumbs = request.GET.get('payload')
            if thumbs not in ['+','-']:
                return JsonResponse(status=500, data={})
        else:
            return JsonResponse(status=500, data={})
    else:
        thumbs = ""

    vote = Vote.objects.create( room = room , thumbs = thumbs, created_date = timezone.now(), attendee = room.attendee_set.get(session=request.session.session_key))
    vote.save()
    return JsonResponse(status=200, data={
        'interval': room.vote_interval.total_seconds()
    })

def status(request, room_id):
    room = Room.objects.get(pk=room_id)
    votes = room.current_vote_count()
    attendees = room.attendee_count()
    if attendees != 0:
        percent = "{:.2f}".format(votes/attendees*100)
    else:
        percent = "0.00%"
    return JsonResponse(status=200, data={
        'votes': votes,
        'attendees': attendees,
        'percent': percent,
        'able_to_vote': room.able_to_vote(request.session.session_key)

    })

def needle_status(request, room_id):
    room = Room.objects.get(pk=room_id)
    thumbs_up_votes = room.thumbs_up_count()
    thumbs_down_votes = room.thumbs_down_count()
    votes = thumbs_up_votes + thumbs_down_votes
    attendees = room.attendee_count()
    if votes != 0:
        percent = "{:.2f}".format(thumbs_up_votes/votes*100)
    else:
        percent = "50.00"
    return JsonResponse(status=200, data={
        'votes': votes,
        'attendees': attendees,
        'percent': percent,
        'able_to_vote': room.able_to_vote(request.session.session_key)

    })
