import turtle
import unittest

from painter import dna_parser
from painter.graphics import actions
from painter.graphics import engine


engine = engine.TurtleEngine()

class TestTurtleAction(unittest.TestCase):

  def setUp(self):
    turtle.reset()

  def __fake_transform(*args):
    len(args)
  __fake_transform.call = lambda *args: len(args)

  def test_call_no_raise(self):
    # Ensure they can all be called without raising an error.
    for ta in actions.TurtleAction:
      # Numbers are always save return values for transforms.
      ta.call(lambda *args: sum(args), [TestTurtleAction.__fake_transform])

  def test_pencolor_r_read(self):
    # Ensure _turtle_color_read is used to transform the outputx.
    ta = actions.TurtleAction.PENCOLOR_R_READ

    # This action doesn't us args.
    ret = ta.call([], [])

    # Default turtle returns color 'black'.
    expected_ret = actions._turtle_color_read('black', 0)
    self.assertEqual(expected_ret, ret)

  def test_turtle_color_read_rbg(self):
    fake_color_ret = (1, 2, 3)
    ret = actions._turtle_color_read(fake_color_ret, 0)
    self.assertEqual(1, ret)
    ret = actions._turtle_color_read(fake_color_ret, 1)
    self.assertEqual(2, ret)
    ret = actions._turtle_color_read(fake_color_ret, 2)
    self.assertEqual(3, ret)
