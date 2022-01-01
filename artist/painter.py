from artist import dna_parser
from artist import stroke

class Painter:

  def __init__(self, dna, graphics_engine):
    self.age = 0.0
    self.raw_dna = str(dna)
    self.graphics_engine = graphics_engine
    self.chromosomes = []
    for chromosome_str in self.raw_dna.split('\n'):
      c = dna_parser.Chromosome(chromosome_str.strip(), self.graphics_engine)
      if c.is_valid():
        self.chromosomes.append(c)
    self.max_age = self.chromosomes[0].post_junk_fun()

  def still_growing(self):
    return self.age <= self.max_age

  def age_up(self):
    self.age += self.chromosomes[0].pre_junk_fun()

  def paint(self):
    for c in self.chromosomes:
      # TODO(kmd): Generate the genes for the inverse side.
      next_stroke = stroke.Stroke(c.pre_junk_fun, c.post_junk_fun)
      for g in dna_parser.GeneSequencer(c):
        next_stroke.add_stroke_action(g)
      next_stroke.apply()
