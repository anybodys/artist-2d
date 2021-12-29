import abc
import datetime
from enum import Enum
import os
import turtle

from PIL import Image

from artist.graphics import actions


class EngineInterface(metaclass=abc.ABCMeta):

  def __init__(self, action_class):
    self.action_class = action_class

  def save_image(self, output_filename: str):
    pass

  def do_action(self, action, *action_args):
    return action(*action_args)

  def get_action(self, index):
    return self.action_class(index)

  def get_action_count(self):
    return len(self.action_class.__members__)


class TurtleEngine(EngineInterface):

  def __init__(self):
    EngineInterface.__init__(self, actions.TurtleAction)
    self.screen = turtle.getscreen()
    self.screen.colormode(255)
    self.turtle = turtle.Turtle()
    self.turtle.speed(10)
    self.turtle.hideturtle()

    self.output_filepath = os.path.join('/', 'tmp', 'artist-2d', f'{datetime.datetime.utcnow()}')
    os.makedirs(os.path.dirname(self.output_filepath), exist_ok=True)
    print(self.output_filepath)

  def do_action(self, action, *action_args):
    action_fun = getattr(self.turtle, action)
    return super().do_action(action_fun, *action_args)

  def save_image(self):
    output_filepath = f'{self.output_filepath}.jpg'
    canvas = self.screen.getcanvas()
    canvas.postscript(file=f'{self.output_filepath}.eps')
    with Image.open(f'{self.output_filepath}.eps') as img:
      img.save(output_filepath)
    return output_filepath
