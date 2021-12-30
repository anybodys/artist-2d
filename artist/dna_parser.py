import random

START_SEQUENCE = 'AAA'
END_SEQUENCE = 'TTT'


class Chromosome():
  def __init__(self, as_str, graphics_engine):
    self.str_rep = as_str
    self.graphics_engine = graphics_engine
    self.pre_junk = ''
    self.post_junk = ''
    self.genes = ''
    self.parse()

  def parse(self):
    assert(not self.is_valid())
    start_index = self.str_rep.find(START_SEQUENCE)
    end_index = self.str_rep.rfind(END_SEQUENCE)
    if not start_index < end_index:
      return

    self.pre_junk = self.str_rep[:start_index]
    self.post_junk = self.str_rep[end_index + len(END_SEQUENCE):]
    self.genes = self.str_rep[start_index + len(START_SEQUENCE):end_index]

    if not self.is_valid():
      print(
        f'Unable to use invalid chromosome: {self}'
      )

    self.pre_junk_fun = random.Random(_dna_as_int(self.pre_junk)).random
    self.post_junk_fun = random.Random(_dna_as_int(self.post_junk)).random

  def is_valid(self):
    return bool(self.pre_junk) and bool(self.post_junk) and bool(self.genes)

  def pre_junk_fun(self):
    return self.pre_junk_fun

  def post_junk_fun(self):
    return self.post_junk_fun

  def __str__(self):
    return (
      f'{self.__class__.__name__} "{self.str_rep}"'
      f'\n  pre-junk: {self.pre_junk}'
      f'\n  post-junk: {self.post_junk}'
      f'\n  genes: {self.genes}')


class GeneSequencer():

  def __init__(self, chromosome):
    self.chromo = chromosome
    self.gene_length = 1 + (_dna_as_int(self.chromo.pre_junk) % 6)

  def __iter__(self):
    self.index = 0
    return self

  def __next__(self):
    if self.index >= len(self.chromo.genes):
      raise StopIteration

    end_i = self.index + (self.gene_length*3)
    gene = self.chromo.genes[self.index:end_i]
    self.index = end_i

    action_index = 1 + (_dna_as_int(gene) % self.chromo.graphics_engine.get_action_count())
    return self.chromo.graphics_engine.get_action(action_index)


def _dna_as_int(as_str):
  return sum(as_str.encode())
