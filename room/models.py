from django.contrib.auth import get_user_model
from django.db import models

from questions.models import Test

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=10, default='')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.test)} {str(self.host)}'


class RoomUsers(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
