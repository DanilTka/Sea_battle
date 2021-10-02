from django.contrib.auth.mixins import LoginRequiredMixin
from django.test import TestCase, Client
from django.urls import reverse


class GameViewsTest(LoginRequiredMixin, TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = Client()
        self.game_lobby_url = reverse('game_lobby')
        self.game_room_url = reverse('game_room', args=['room_test'])
        self.client.login(username="testing", password='12345test')

    def test_game_logged_GET(self):
        response = self.client.get(self.game_lobby_url)

        self.assertEqual(response.status_code, 200)

    def test_game_room_logged_GET(self):
        response = self.client.get(self.game_room_url)

        self.assertEqual(response.status_code, 200)

    def test_game_POST_shuffle(self):
        response = self.client.post(self.game_lobby_url, {
            'shuffle': 'shuffle'
        })
        self.assertTrue(response.status_code == 302 or response.status_code == 200)

    def test_game_POST_find_opponent(self):
        response = self.client.post(self.game_lobby_url, {
            'find_opponent': 'find_opponent'
        })
        self.assertRedirects(response, reverse('game_room', args=['room_test']))

    def test_game_room_POST_to_lobby(self):
        response = self.client.post(self.game_room_url)

        self.assertEqual(response.status_code, 200)

    def test_game_anonymous_GET(self):
        self.client.logout()
        response = self.client.get(self.game_lobby_url)

        self.assertEqual(response.status_code, 302)

    def test_game_room_anonymous_GET(self):
        self.client.logout()
        response = self.client.get(self.game_room_url)

        self.assertEqual(response.status_code, 302)
