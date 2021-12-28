import datetime
import sys
import turtle

from PIL import Image

from artist import dna_parser as DP
from artist.graphics import engine
from artist.storage import art_storage
from artist import stroke

# TODO(kmd): Don't hard code. :)
dna_in = '/home/kmd/Projects/anybodys/artist/artist/data/dna/demo.txt'

def main() -> int:
  graphics_engine = engine.TurtleEngine()

  dna_parser = DP.Parser(graphics_engine)
  chromosomes = dna_parser.parse_file(dna_in)

  MAX_GROWTH = 4
  # While: Still growing, make and apply new strokes.
  for i in range(MAX_GROWTH):
    print(f'****year {i}****')
    for c in chromosomes:
      next_stroke = stroke.Stroke(c.pre_junk_fun, c.post_junk_fun)
      for g in DP.GeneSequencer(c):
        next_stroke.add_stroke_action(g)

      next_stroke.apply()

  # Save this image.
  tmp_filepath = graphics_engine.save_image()
  art_storage.ArtStorage(0).upload_blob(tmp_filepath)
  return 0


if __name__ == '__main__':
    sys.exit(main())
