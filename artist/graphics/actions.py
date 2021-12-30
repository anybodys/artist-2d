from collections.abc import Callable
from enum import Enum
from functools import partial
import turtle

class ActionType(Enum):
  MOVE = 1
  BRUSH = 2
  READ = 3


class Action(Enum):

  def __new__(cls, action_type, action_callable, arg_transforms, output_transform=None):
    value = len(cls.__members__) + 1
    obj = object.__new__(cls)
    obj._value_ = value
    obj.action_type = action_type
    obj.action = action_callable
    obj.arg_transforms = arg_transforms
    obj.output_transform = output_transform
    return obj

  def call(self, arg_generator, semantic_context):
    #print(f'calling {self} with {arg_generator}')
    args = []
    for arg_t in self.arg_transforms:
      next_arg = self._get_next_arg(arg_generator, semantic_context)
      args.append(arg_t(next_arg))
    ret = self.action(*args)
    if self.output_transform:
      ret = self.output_transform(ret)
    return ret

  def _get_next_arg(self, arg_gen: Callable, semantic_context):
    ret = arg_gen()
    if semantic_context:
      # Use the generated arg to pick a semantic function.
      semantic_function = semantic_context[int(ret * len(semantic_context))]
      # Since it's a semantic function, there should be no args to generate and no semantic context.
      ret = semantic_function.call(None, [])
    ret = float(ret)
    if ret < 0.0:
      ret *= -1.0
    # Convert to [0.0,1.0]
    while ret > 1.0:
      ret /= 10.0
    return ret


################################################################
## Handy Action transform functions for reuse.
################################################################
def _position(x):
  return int(x*200) - 100

def _angle(x):
  return int(x*360)

def _color(x):
  return int(x*255)

def _turtle_color_read(fun, field):
  # Default value is 'black' as a string. Manually convert.
  color = fun()
  if color == 'black':
    return 0
  # Otherwise, this should be an RGB tuple.
  return color[field]


class TurtleAction(Action):
  # Movements
  FORWARD = (ActionType.MOVE, turtle.forward, [_position])
  BACKWARD = (ActionType.MOVE, turtle.backward, [_position])
  RIGHT = (ActionType.MOVE, turtle.right, [_angle])
  LEFT = (ActionType.MOVE, turtle.left, [_angle])
  GOTO = (ActionType.MOVE, turtle.goto, [_position, _position])
  SETX = (ActionType.MOVE, turtle.setx, [_position])
  SETY = (ActionType.MOVE, turtle.sety, [_position])
  SETHEADING = (ActionType.MOVE, turtle.setheading, [_angle])
  HOME = (ActionType.MOVE, turtle.home, [])
  CIRCLE = (ActionType.MOVE, turtle.circle, [_position, _angle, lambda x: int(x*99) + 1])
  DOT = (ActionType.MOVE, turtle.dot, [lambda x: int(x*50), _color, _color, _color])
  UNDO = (ActionType.MOVE, turtle.undo, [])
  TOWARDS = (ActionType.MOVE, turtle.towards, [_position, _position])

  # Brush configuration
  PENDOWN = (ActionType.BRUSH, turtle.pendown, [])
  PENUP = (ActionType.BRUSH, turtle.penup, [])
  PENSIZE = (ActionType.BRUSH, turtle.pensize, [lambda x: int(x*50)])
  PENCOLOR = (ActionType.BRUSH, turtle.pencolor, [_color, _color, _color])
  BEGIN_FILL = (ActionType.BRUSH, turtle.begin_fill, [])
  END_FILL = (ActionType.BRUSH, turtle.end_fill, [])

  # Read.
  XCOR = (ActionType.READ, turtle.xcor, [])
  YCOR = (ActionType.READ, turtle.ycor, [])
  ISDOWN = (ActionType.READ, turtle.isdown, [])
  PENCOLOR_R_READ = (ActionType.READ, partial(_turtle_color_read, turtle.pencolor, 0), [])
  PENCOLOR_G_READ = (ActionType.READ, partial(_turtle_color_read, turtle.pencolor, 1), [])
  PENCOLOR_B_READ = (ActionType.READ, partial(_turtle_color_read, turtle.pencolor, 2), [])
  FILLCOLOR_R_READ = (ActionType.READ, partial(_turtle_color_read, turtle.fillcolor, 0), [])
  FILLCOLOR_G_READ = (ActionType.READ, partial(_turtle_color_read, turtle.fillcolor, 1), [])
  FILLCOLOR_B_READ = (ActionType.READ, partial(_turtle_color_read, turtle.fillcolor, 2), [])
  FILLING = (ActionType.READ, turtle.filling, [])

