from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Room, Vote, Attendee


admin.site.register(Vote)
admin.site.register(Attendee)
admin.site.register(Session)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'created_date', 'vote_interval')
    ordering = ['created_date']

admin.site.register(Room, RoomAdmin)
