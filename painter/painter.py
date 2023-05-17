from painter import dna_parser
from painter import stroke

class Painter:

  def __init__(self, dna, graphics_engine):
    self.age = 0.0
    self.raw_dna = str(dna)
    self.graphics_engine = graphics_engine
    self.chromosomes = []
    for chromosome_str in self.raw_dna.split('\n'):
      c1 = dna_parser.Chromosome(chromosome_str.strip(), self.graphics_engine)
      c2 = dna_parser.Chromosome(chromosome_str.strip(), self.graphics_engine, inverse=True)
      if c1.is_valid() and c2.is_valid():
        self.chromosomes.append((c1, c2))
    self.max_age = self.chromosomes[0][0].post_junk_fun()

  def still_growing(self):
    return self.age <= self.max_age

  def age_up(self):
    self.age += self.chromosomes[0][0].pre_junk_fun()

  def paint(self):
    for c1, c2 in self.chromosomes:
      self.paint_stroke(c1)
      self.paint_stroke(c2)

  def paint_stroke(self, c):
    next_stroke = stroke.Stroke(c.pre_junk_fun, c.post_junk_fun)
    for g in dna_parser.GeneSequencer(c):
      next_stroke.add_stroke_action(g)
    next_stroke.apply()
