from unittest import mock

from django.test import TestCase
from django.test.client import Client

from api import models
from painter import generation


class TestViews(TestCase):

  def setUp(self):
    self.client = Client()

    graphics_engine_patch = mock.patch('painter.graphics.engine.TurtleEngine')
    self.engine = graphics_engine_patch.start().return_value
    self.addCleanup(graphics_engine_patch.stop)

    # Make sure we don't talk to the real storage system.
    art_storage_patch = mock.patch('painter.generation.art_storage')
    self.art_storage = art_storage_patch.start().ArtStorage.return_value
    self.addCleanup(art_storage_patch.stop)

    painter_patch = mock.patch('painter.painter.Painter')
    self.painter = painter_patch.start().return_value
    # Make sure it doesn't grow indefinitely. :)
    self.painter.still_growing.return_value = False
    self.addCleanup(painter_patch.stop)

  def test_health(self):
    response = self.client.get('/painter/health')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'OK')

  def test_crontime_bootstrap(self):
    # Ensure we have no generations (which triggers the bootstrap).
    models.Generation.objects.all().delete()
    self.assertEqual(models.Generation.objects.count(), 0)

    response = self.client.get('/painter/crontime')

    # Check the HTTP call succeeded.
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'OK')

    # The first generation should have been created.
    self.assertEqual(models.Generation.objects.count(), 1)

    # The engine should have been reset once per artist.
    self.assertEqual(self.engine.reset.call_count, generation._NUM_ARTISTS)
    # And that we saved one image per artists.
    self.assertEqual(self.engine.save_image.call_count, generation._NUM_ARTISTS)
