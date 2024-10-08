import unittest

from painter import dna_parser
from painter.graphics import engine


class TestChromosome(unittest.TestCase):

    def test_parse_valid(self):
      c = dna_parser.Chromosome('GAAACGCTTTC', engine.TurtleEngine())
      self.assertTrue(c.is_valid())
      self.assertEqual('G', c.pre_junk)
      self.assertEqual('C', c.post_junk)
      self.assertEqual('CGC', c.genes)


class TestGeneSequencer(unittest.TestCase):

    def test_valid(self):
      c = dna_parser.Chromosome('', engine.TurtleEngine())
      c.pre_junk = 'A'  # 65 % 6 = 5
      c.genes = 'AAACCCTTTAAACCC'

      gs = dna_parser.GeneSequencer(c)
      all_genes = list(gs)
      self.assertEqual(1, len(all_genes))
