from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from game import views
from game.models import Fields, Player, Room, Message


class ModelTest(TestCase):
    def setUp(self):
        self.field = Fields.objects.create(id=1,
                                           fields='0111101110000000000010000000010000000001100000000010000000010000000000100000000000000000000110101110')
        self.room = Room.objects.create(
            name='room_test',
            id=1,
        )
        self.player = Player.objects.create(
            username='test',
            field=self.field,
            room=self.room
        )
        messages = []
        for i in range(100):
            messages.append(Message.objects.create(
                player=self.player.username,
                content=f'{i}',
                room_name=self.room.name
            ))
        self.messages = messages

    def test_load_messages(self):
        messages = Message.load_messages(self.room.name)
        self.assertTrue(messages[0].timestamp < messages[49].timestamp)
        self.assertTrue(messages[49].timestamp < messages[99].timestamp)

    def test_message_str(self):
        self.assertEqual(
            self.messages[0].__str__(),
            "{}  time: {}".format(self.messages[0].content, format(self.messages[0].timestamp, "%H:%M:%S"))
        )
