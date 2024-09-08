from unittest import mock

from django.test import TestCase
from django.test.client import Client

from api import models


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

  def test_vote(self):
    test_user = models.VotingUser.objects.create(
      user=models.User.objects.create(),
    )
    self.client.force_login(test_user.user, backend=None)
    test_art = models.Art.objects.create(
      public_link='http://test.url',
      generation=models.Generation.objects.create(),
      artist=models.Artist.objects.create(),
    )

    response = self.client.post(
      '/api/vote',
      {'art': test_art.id},
    )

    # Validate that it returned success & empty response.
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {})
    # And it saved a vote to the DB. Get should run without throwing an error.
    models.Vote.objects.get(user=test_user, art=test_art)

  def test_vote_unauthed(self):
    test_art = models.Art.objects.create(
      public_link='http://test.url',
      generation=models.Generation.objects.create(),
      artist=models.Artist.objects.create(),
    )

    response = self.client.post(
      '/api/vote',
      {'art': test_art.id},
    )

    # Validate that it returned a redirect.
    self.assertEqual(response.status_code, 302)
    # And it did not save a vote.
    self.assertEqual(0, models.Vote.objects.count())
