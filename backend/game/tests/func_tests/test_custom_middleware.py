from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from main.middleware.exception_middleware import MyExceptionMiddleware
from game.models import Message, Player, Room


class CustomMiddlewareTest(LoginRequiredMixin, TestCase):
    fixtures = ['test_data.json']
    @classmethod
    def setUpTestData(cls):
        Room.objects.create(
            name="test"
        )
        Player.objects.create(
            username="test"
        )
        Message.objects.create(
            player="test",
            room_name="test"
        )

    def setUp(self):
        self.client = Client()
        self.game_room_url = reverse('game_room', args=['room1'])
        self.client.login(username="testing", password='12345test')
        self.request = RequestFactory().get(self.game_room_url)

    def test_exception_middleware(self):
        try:
            res = self.client.get(self.game_room_url)
            Room.objects.get(name="room1")
        except ObjectDoesNotExist as e:
            MyExceptionMiddleware(res).process_exception(self.request, e)
        finally:
            self.assertEqual(Room.objects.filter().first(), None)
            self.assertEqual(Player.objects.filter().first(), None)
            self.assertEqual(Message.objects.filter().first(), None)
