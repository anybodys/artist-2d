import abc
import io
import tempfile
import turtle

from PIL import Image

from painter.graphics import actions


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

  def __new__(cls):
    """Create or return the singleton instance of the ArtStorage."""
    if not hasattr(cls, 'instance'):
      cls.instance = super(TurtleEngine, cls).__new__(cls)
    return cls.instance

  def __init__(self):
    EngineInterface.__init__(self, actions.TurtleAction)
    self.reset()

  def save_image(self, storage, generation: int, artist_id: int):
    """Save a JPEG image to the art_storage.

    Args:
    - storage: The object responsible for storaging images.
    - generation: The generation number, used by `storage` to know where to save the image.
    - artist_id: The artist's numeric ID, used by `storage` to know where to save the image.

    Returns:
    - str: The public URL to the newly saved image file.
    """
    canvas = turtle.getscreen().getcanvas()
    ps = canvas.postscript()
    image_file = storage.new_image_file(generation, artist_id)
    with Image.open(io.BytesIO(ps.encode('utf-8'))) as img:
      with storage.open(image_file) as fp:
        img.save(fp, format='JPEG')
    return image_file.public_url

  def reset(self):
    turtle.clearscreen()
    turtle.speed(10)
    turtle.hideturtle()
    turtle.getscreen().colormode(255)
