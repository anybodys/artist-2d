import datetime
import random
import sys
import turtle

from PIL import Image

import dna_parser as DP
import stroke
import turtle_function as TF

dna_in = '/home/kmd/Projects/anybodys/artist/in/demo.txt'

def main() -> int:
  # Create a canvas on which to draw
  s = turtle.getscreen()
  s.colormode(255)
  t = turtle.Turtle()
  t.speed(10)

  MAX_GROWTH = 50
  # While: Still growing, make and apply new strokes.
  for i in range(MAX_GROWTH):
    dna_parser = DP.Parser()
    chromosomes = dna_parser.parse_file(dna_in)
    # Sequence "junk DNA" should be arg_generator details.... For now, random.
    arg_generator_fn = random.random
    next_stroke = stroke.Stroke(arg_generator_fn)
    for c in chromosomes:
      for g in DP.GeneSequencer(c):
        next_stroke.add_function(g)

    next_stroke.apply()

    # Save this image.
    out_filename = f'/home/kmd/Projects/anybodys/artist/out/random{datetime.datetime.utcnow().isoformat()}'
    canvas = s.getcanvas()
    canvas.postscript(file=f'{out_filename}.eps')
    img = Image.open(f'{out_filename}.eps')
    img.save(f'{out_filename}.jpg')
    return 0


if __name__ == '__main__':
    sys.exit(main())