from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Room, Vote, Attendee

admin.site.register(Room)
admin.site.register(Vote)
admin.site.register(Attendee)
admin.site.register(Session)
