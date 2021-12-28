import abc
from enum import Enum
import turtle

from PIL import Image

from artist.graphics import actions


class EngineInterface(metaclass=abc.ABCMeta):

  def __init__(self, action_class):
    self.action_class = action_class

  def save_image(self, output_filename: str):
    pass

  def get_action(self, index):
    return self.action_class(index)


class TurtleEngine(EngineInterface):

  def __init__(self):
    EngineInterface.__init__(self, actions.TurtleAction)
    self.screen = turtle.getscreen()
    self.screen.colormode(255)
    self.turtle = turtle.Turtle()
    self.turtle.speed(10)
    self.turtle.hideturtle()


  def save_image(self, output_filename: str):
    canvas = self.screen.getcanvas()
    canvas.postscript(file=f'{output_filename}.eps')
    img = Image.open(f'{output_filename}.eps')
    img.save(f'{output_filename}.jpg')
