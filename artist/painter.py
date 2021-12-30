from artist import dna_parser
from artist import stroke

class Painter:

  def __init__(self, dna, graphics_engine):
    self.age = 0
    self.raw_dna = str(dna)
    self.graphics_engine = graphics_engine
    self.chromosomes = [
      dna_parser.Chromosome(chromosome_str.strip(), self.graphics_engine)
      for chromosome_str in self.raw_dna.split('\n')
    ]

  def still_growing(self):
    # TODO(kmd): Make max age based on DNA.
    if self.age > 3:
      return False
    return True

  def age_up(self):
    self.age += 1

  def paint(self):
    for c in self.chromosomes:
      if not c.is_valid():
        continue
      # TODO(kmd): Generate the genes for the inverse side.
      next_stroke = stroke.Stroke(c.pre_junk_fun, c.post_junk_fun)
      for g in dna_parser.GeneSequencer(c):
        next_stroke.add_stroke_action(g)
      next_stroke.apply()
