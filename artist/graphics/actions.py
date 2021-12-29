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

  def call(self, engine, arg_generator, semantic_context):
    print(f'calling {self} with {arg_generator}')
    args = self._generate_args(engine, arg_generator, semantic_context)
    ret = engine.do_action(self.action, *list(args))
    # Semantic functions (reads) may have transforms on their return values.
    return self._transform_action_output(ret)

  def _generate_args(self, engine, arg_generator, semantic_context):
    for arg_t in self.arg_transforms:
      next_arg = self._get_next_arg(engine, arg_generator, semantic_context)
      yield arg_t(next_arg)

  def _get_next_arg(self, engine, arg_gen: Callable, semantic_context):
    ret = arg_gen()
    if semantic_context:
      # Use the generated arg to pick a semantic function.
      semantic_function = semantic_context[int(ret * len(semantic_context))]
      # Since it's a semantic function, there should be no args to generate and no semantic context.
      ret = semantic_function.call(engine, None, [])
    ret = float(ret)
    if ret < 0.0:
      ret *= -1.0
    # Convert to [0.0,1.0]
    while ret > 1.0:
      ret /= 10.0
    return ret

  def _transform_action_output(self, ret):
    if self.output_transform:
      ret = self.output_transform(ret)
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

def _turtle_color_read(color, field):
  # Default value is 'black' as a string. Manually convert.
  if color == 'black':
    return 0
  # Otherwise, this should be an RGB tuple.
  return color[field]


class TurtleAction(Action):
  # Movements
  FORWARD = (ActionType.MOVE, 'forward', [_position])
  BACKWARD = (ActionType.MOVE, 'backward', [_position])
  RIGHT = (ActionType.MOVE, 'right', [_angle])
  LEFT = (ActionType.MOVE, 'left', [_angle])
  GOTO = (ActionType.MOVE, 'goto', [_position, _position])
  SETX = (ActionType.MOVE, 'setx', [_position])
  SETY = (ActionType.MOVE, 'sety', [_position])
  SETHEADING = (ActionType.MOVE, 'setheading', [_angle])
  HOME = (ActionType.MOVE, 'home', [])
  CIRCLE = (ActionType.MOVE, 'circle', [_position, _angle, lambda x: int(x*99) + 1])
  DOT = (ActionType.MOVE, 'dot', [lambda x: int(x*50), _color, _color, _color])
  UNDO = (ActionType.MOVE, 'undo', [])
  TOWARDS = (ActionType.MOVE, 'towards', [_position, _position])

  # Brush configuration
  PENDOWN = (ActionType.BRUSH, 'pendown', [])
  PENUP = (ActionType.BRUSH, 'penup', [])
  PENSIZE = (ActionType.BRUSH, 'pensize', [lambda x: int(x*50)])
  PENCOLOR = (ActionType.BRUSH, 'pencolor', [_color, _color, _color])
  BEGIN_FILL = (ActionType.BRUSH, 'begin_fill', [])
  END_FILL = (ActionType.BRUSH, 'end_fill', [])

  # Read.
  XCOR = (ActionType.READ, 'xcor', [])
  YCOR = (ActionType.READ, 'ycor', [])
  ISDOWN = (ActionType.READ, 'isdown', [])
  PENCOLOR_R_READ = (ActionType.READ, 'pencolor', [], lambda r: _turtle_color_read(r, 0))
  PENCOLOR_G_READ = (ActionType.READ, 'pencolor', [], lambda r: _turtle_color_read(r, 1))
  PENCOLOR_B_READ = (ActionType.READ, 'pencolor', [], lambda r: _turtle_color_read(r, 2))
  FILLCOLOR_R_READ = (ActionType.READ, 'fillcolor', [], lambda r: _turtle_color_read(r, 0))
  FILLCOLOR_G_READ = (ActionType.READ, 'fillcolor', [], lambda r: _turtle_color_read(r, 1))
  FILLCOLOR_B_READ = (ActionType.READ, 'fillcolor', [], lambda r: _turtle_color_read(r, 2))
  FILLING = (ActionType.READ, 'filling', [])

