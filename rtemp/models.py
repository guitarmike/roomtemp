from django.db import models
from django.utils import timezone


class Room(models.Model):
    owner = models.ForeignKey('auth.User')
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.text
