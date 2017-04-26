from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Room

# Create your views here.
def home(request):
    return render(request, 'rtemp/home.html', {})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'rtemp/detail.html', {'room':room})
