from django.test import SimpleTestCase
from django.urls import reverse, resolve

from game import views


class GameUrlTest(SimpleTestCase):
    def setUp(self):
        self.game_lobby_url = reverse('game_lobby')
        self.game_room_url = reverse('game_room', args=['room_test'])

    def test_game_url_resolves(self):
        self.assertEqual(resolve(self.game_lobby_url).func, views.game)

    def test_game_room_url_resolves(self):
        self.assertEqual(resolve(self.game_room_url).func, views.game_room)