import unittest
from unittest import mock

import pytest


@pytest.mark.usefixtures("client")
class TestApi(unittest.TestCase):

  @pytest.fixture(autouse=True)
  def setClient(self, client):
    self.client = client

  def setUp(self):
    storage_patcher = mock.patch('voting.api.art_storage')
    self.mock_storage = storage_patcher.start().get_api()
    self.addCleanup(storage_patcher.stop)

  def test_get_health(self):
    response = self.client.get('/health')
    assert 'OK' == response.json['status']
    assert 200 == response.status_code

  def test_get_art(self):
    art_response = {'art': [{
      'artist_id': 'fake-artist1',
      'generation': 19,
      'public_link': 'fake-image-url',
    }]}
    self.mock_storage.get_art.return_value = art_response

    response = self.client.get('/art')

    assert 200 == response.status_code
    assert art_response == response.json
