import abc
import io
import tempfile
import turtle

from PIL import Image

from artist.graphics import actions
from artist.storage import art_storage


class EngineInterface(metaclass=abc.ABCMeta):

  def __init__(self, action_class):
    self.action_class = action_class

  def save_image(self, output_filename: str):
    pass

  def get_action(self, index):
    return self.action_class(index)

  def get_action_count(self):
    return len(self.action_class.__members__)


class TurtleEngine(EngineInterface):

  def __init__(self):
    EngineInterface.__init__(self, actions.TurtleAction)
    self.art_storage = art_storage.ArtStorage()
    self.reset()

  def save_image(self, generation, artist_id):
    canvas = turtle.getscreen().getcanvas()
    ps = canvas.postscript()
    with Image.open(io.BytesIO(ps.encode('utf-8'))) as img:
      with self.art_storage.open(generation, artist_id) as blob_fp:
        img.save(blob_fp, format='JPEG')

  def reset(self):
    turtle.clearscreen()
    turtle.speed(10)
    turtle.hideturtle()
    turtle.getscreen().colormode(255)
