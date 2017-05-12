import datetime
from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse


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
    code = models.CharField(max_length=8, default="",unique=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('detail',kwargs={'room_id':self.id})

    def makeCode(self):
        try:
            self.code = get_random_string(length=5, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        except IntegrityError:
            self.makeCode()
        return self.save()

    def authenticate_attendee(self, key):
        try:
            att = self.attendee_set.get(session=key)
            att.last_action = timezone.now()
            att.save()
            return True
        except ObjectDoesNotExist:
            return False

    def add_attendee(self, key):
        self.attendee_set.create(
            room=self,
            session=key,
            last_action = timezone.now()
        )
        return True

    def attendee_count(self):
        return self.attendee_set.filter(last_action__range=(timezone.now() - datetime.timedelta(minutes = 5), timezone.now())).count()

    def current_vote_count(self):
        return self.vote_set.filter(created_date__range=(timezone.now() - self.vote_interval, timezone.now())).count()

    def thumbs_up_count(self):
        return self.vote_set.filter(thumbs__exact =  "+").filter(created_date__range=(timezone.now() - self.vote_interval, timezone.now())).count()

    def thumbs_down_count(self):
        return self.vote_set.filter(thumbs = "-").filter(created_date__range=(timezone.now() - self.vote_interval, timezone.now())).count()

    def able_to_vote(self, key):
        att = self.attendee_set.get(session=key)
        try:
            last_vote = att.vote_set.latest('created_date')
        except ObjectDoesNotExist:
            return True
        return last_vote.created_date+self.vote_interval<=timezone.now()

    def owned_by(self, user):
        return self.owner == user

    def show_widget(self, user):
        return self.owned_by(user) or (self.public == True)


class Attendee(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    last_action = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=300, default="")

class Vote(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, default="9")
    created_date = models.DateTimeField(default=timezone.now)

    THUMBS_UP_DOWN = (
        ('+', 'Thumbs Up'),
        ('-', 'Thumbs Down'),
    )

    thumbs = models.CharField(max_length=1, choices=THUMBS_UP_DOWN, blank=True, help_text='Thumbs up/down')

    def __str__(self):
        return self.room.text+": "+self.thumbs
