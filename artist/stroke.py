from artist.graphics import actions

class Stroke:

  def __init__(self, brush_args, move_args):
    self.brush_args = brush_args
    self.move_args = move_args
    self.brush = []
    self.movement = []
    self.semantics = []

  def add_stroke_action(self, stroke_action):
    if stroke_action.action_type == actions.ActionType.BRUSH:
      self.brush.append(stroke_action)
    elif stroke_action.action_type == actions.ActionType.MOVE:
      self.movement.append(stroke_action)
    elif stroke_action.action_type == actions.ActionType.READ:
      self.semantics.append(stroke_action)
    else:
      print(f'Ignoring uncategorizable function {stroke_action.__name__}')

  def apply(self, graphics_engine):
    for b in self.brush:
      b.call(graphics_engine, self.brush_args, self.semantics)
    for m in self.movement:
      m.call(graphics_engine, self.move_args, self.semantics)
