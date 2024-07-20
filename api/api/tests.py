from unittest import mock

from django.test import TestCase
from django.test.client import Client

class TestApi(TestCase):

  def setUp(self):
    self.client = Client()

    art_storage_patch = mock.patch('api.art_storage.ArtStorage')
    self.art_storage = art_storage_patch.start().return_value
    self.addCleanup(art_storage_patch.stop)

  def test_health(self):
    response = self.client.get('/api/health')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'OK')

  def test_art_get(self):
    self.art_storage.get_art.return_value = {}

    response = self.client.get('/api/art')

    # No params should use the current gen in the DB.
    self.art_storage.get_art.assert_called_with(0)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {})

  def test_art_get_query_param_gen(self):
    self.art_storage.get_art.return_value = {}

    response = self.client.get('/api/art?gen=19')

    # No params should use the current gen in the DB.
    self.art_storage.get_art.assert_called_with(19)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {})
