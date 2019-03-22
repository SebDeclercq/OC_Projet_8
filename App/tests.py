from django.http import HttpResponse
from django.test import Client, TestCase


class TestAppViews(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()

    def test_get_home_page(self) -> None:
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
