from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from users import views


class UsersUrlTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_register_url_resolves(self):
        self.assertEqual(resolve(self.register_url).func, views.register)

    def test_login_url_resolves(self):
        self.assertEqual(resolve(self.login_url).func, views.user_login)

    def test_logout_url_resolves(self):
        self.assertEqual(resolve(self.logout_url).func.view_class, auth_views.LogoutView)
