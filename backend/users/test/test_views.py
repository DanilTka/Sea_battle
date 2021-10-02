from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from game.models import Room, Player


class UsersUrlTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testqwe', password='123456789')
        self.game_lobby_url = reverse('game_lobby')
        self.game_room_url = reverse('game_room', args=['room_test'])
        self.room = Room.objects.create(name='room_test')
        self.player = Player.objects.create(username='test')
        self.factory = RequestFactory()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/logout.html')


    def test_login_POST_redirect(self):
        response = self.client.post(self.login_url,
                                    data={
                                        'username': 'testqwe',
                                        'password': '123456789',
                                    })
        self.assertRedirects(response, reverse('game_lobby'))


    def test_register_POST_redirect(self):
        response = self.client.post(self.register_url,
                                    data={
                                        'username': 'adqwer',
                                        'password1': 'test123321qwe',
                                        'password2': 'test123321qwe'
                                    })
        self.assertRedirects(response, reverse('game_lobby'))
