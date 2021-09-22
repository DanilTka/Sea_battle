from django.test import TestCase

from game.models import Fields, Player, Room


class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Player.objects.create(
            username='test',
            field = Fields.objects.get(id=1),
            room = Room.objects.create(
                name='room_test',
                id=1000,
            )
        )
