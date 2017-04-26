import datetime
from django.db import models
from django.utils import timezone


class Room(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(
            default=timezone.now)

    TYPES = (
        ('b', 'Binary Room'),
        ('q', 'Quad Room'),
        ('t', 'Thermometer'),
        ('n', 'Needle'),
    )

    room_type = models.CharField(max_length=1, choices=TYPES, blank=True, default='t', help_text='Room type')
    feed = models.CharField(max_length=300, default="")
    caption_1 = models.CharField(max_length=120, default="")
    caption_2 = models.CharField(max_length=120, default="")
    caption_3 = models.CharField(max_length=120, default="")
    caption_4 = models.CharField(max_length=120, default="")
    vote_interval =  models.DurationField(default=datetime.timedelta(minutes=1))
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.text
