import random

from api import art_storage
from api import models
from painter.graphics import engine
from painter import painter as _painter


_GRAPHICS_ENGINE = None

def graphics_engine():
  global _GRAPHICS_ENGINE
  if not _GRAPHICS_ENGINE:
    _GRAPHICS_ENGINE = engine.TurtleEngine()
  return _GRAPHICS_ENGINE


# Hardcode a few special values because they're just used once.
_NUM_ARTISTS = 64
_NUM_CHROMOSOMES = 32
_MIN_CHROMOSOME_LENGTH = 256
_MAX_CHROMOSOME_LENGTH = 512


def bootstrap():
  """Create a first generation of artists.
  """
  gen = models.Generation.objects.create()

  for i in range(_NUM_ARTISTS):
    # Build the DNA string of chromosomes.
    chromosomes = []
    for _ in range(_NUM_CHROMOSOMES):
      chromo_len = random.randint(_MIN_CHROMOSOME_LENGTH, _MAX_CHROMOSOME_LENGTH-1)
      chromo_str = ''.join(random.choices('ATCG', k=chromo_len))
      chromosomes.append(chromo_str)

    dna = '\n'.join(chromosomes)
    artist = models.Artist.objects.create(
      dna=dna,
      generation=gen,
    )
    paint(artist, gen)


def paint(artist, gen):
  """Paints and saves this artist's masterpiece to the artist model.
  """
  graphics_engine().reset()
  p = _painter.Painter(artist.dna, graphics_engine())
  while p.still_growing():
    p.paint()
    p.age_up()
  public_url = graphics_engine().save_image(art_storage.ArtStorage(), gen.id, artist.id)
  artist.public_url = public_url
  artist.save()
