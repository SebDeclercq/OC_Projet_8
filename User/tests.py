from typing import Any
from django.http import HttpRequest, HttpResponse
from django.test import Client, TestCase
from django.urls import resolve
from .models import User
from .views import LoginView


class LogInTest(TestCase):
    URL: str = '/user/login'

    def setUp(self) -> None:
        self.client: Client = Client()
        self.valid_password: str = 'azerty'
        self.user: User = User.objects.create_user(
            email='az@er.ty', password=self.valid_password
        )
        print(self.user.password)

    def test_url_resolve_login(self) -> None:
        self.assertEqual(
            resolve(self.URL).func.view_class, LoginView  # type: ignore
        )

    def test_page_return_expected_html(self) -> None:
        response: HttpResponse = self.client.get(self.URL)
        html: str = response.content.decode('utf8').strip('\n')
        self.assertTrue(html.startswith('<!DOCTYPE'))
        self.assertIn('<title>Log in</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_login_valid_credentials(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'email': self.user.email, 'password': self.valid_password
        })
        html: str = response.content.decode('utf8')
        self.assertIn(f'AS {self.user.email}', html)

    def test_login_invalid_credentials(self) -> None:
        response: HttpResponse = self.client.post(self.URL, {
            'email': self.user.email, 'password': 'wrong_password'
        })
        html: str = response.content.decode('utf8')
        self.assertIn('WRONG CREDENTIALS, PLEASE RETRY', html)
