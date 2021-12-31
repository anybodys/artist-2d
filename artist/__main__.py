import datetime
import sys
import turtle

from PIL import Image

from artist import painter
from artist import datastore
from artist.graphics import engine
from artist.storage import art_storage

def main() -> int:
  graphics_engine = engine.TurtleEngine(art_storage.ArtStorage())
  DS = datastore.Client()

  current_gen = 0
  for artist_id, dna_str in DS.read_dna(current_gen):
    print(f'Artist {artist_id} starting to paint...')
    graphics_engine.reset()
    p = painter.Painter(dna_str, graphics_engine)
    while p.still_growing():
      p.paint()
      p.age_up()
    graphics_engine.save_image(current_gen, artist_id)
  return 0


if __name__ == '__main__':
    sys.exit(main())
