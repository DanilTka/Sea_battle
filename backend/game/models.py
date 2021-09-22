from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Message(models.Model):
    player = models.CharField(max_length=30)
    content = models.TextField()
    room_name = models.CharField(max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content, format(self.timestamp, "%H:%M:%S")

    def load_messages(room_name):
        return Message.objects.order_by('timestamp').filter(
            room_name=room_name
        )[:100]


class Fields(models.Model):
    fields = models.CharField(max_length=150)


class Player(models.Model):
    username = models.CharField(max_length=30)
    field = models.CharField(max_length=150)
    room = models.CharField(max_length=5, null=True)
    channel_name = models.CharField(max_length=255, null=True)
    is_in_the_room = models.BooleanField(default=False)


class Room(models.Model):
    name = models.CharField(max_length=5)
    first_field = models.CharField(max_length=150, null=True)
    second_field = models.CharField(max_length=150, null=True)
    first_user = models.ForeignKey(
        Player,
        related_name='related_field_for_the_first',
        on_delete=models.CASCADE,
        null=True
    )
    second_user = models.ForeignKey(
        Player,
        related_name='related_field_for_the_second',
        on_delete=models.CASCADE,
        null=True
    )
    whos_turn = models.ForeignKey(
        Player,
        related_name='turn',
        on_delete=models.CASCADE,
        null=True
    )
    first_count = models.IntegerField(default=0)
    second_count = models.IntegerField(default=0)
    group_channel_name = models.CharField(max_length=255, null=True)


    def __str__(self):
        return "{}".format(self.name)