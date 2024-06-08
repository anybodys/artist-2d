from django.test import TestCase
from django.test.client import Client

class TestApi(TestCase):

  def setUp(self):
    self.client = Client()

  def test_health(self):
    response = self.client.get('/api/health')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'OK')
