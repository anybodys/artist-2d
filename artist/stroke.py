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
      print(f'Ingoring uncategorizable function {stroke_action.__name__}')

  def apply(self):
    for b in self.brush:
      b.call(self.brush_args, self.semantics)
      #self._apply(b, self.brush_args)
    for m in self.movement:
      m.call(self.move_args, self.semantics)
      #self._apply(m, self.move_args)

  def off_apply(self, s, arg_gen):
    args = []
    for arg_transform in s.arg_transforms:
      args.append(arg_transform(self._next_arg(arg_gen)))
    #print(f'{s.function}({args})')
    s.function(*args)

  def off_next_arg(self, arg_gen):
    sem_fun = self.semantics[int(arg_gen() * len(self.semantics))]
    ret = sem_fun.function()
    # If this can be encoded (e.g., str->byte[]), encode it.
    if hasattr(ret, 'encode'):
      ret = ret.encode()
    # If we have more than one thing, but a random element.
    if hasattr(ret, '__iter__'):
      ret = ret[int(arg_gen() * len(ret))]
    ret = float(ret)
    if ret < 0.0:
      ret *= -1.0
    # Convert to [0.0,1.0]
    while ret > 1.0:
      ret /= 10.0
    # Let's get fancy! We could have a binary value here (0 or 1). That generally kills all fun.
    # Let's shift that down halfway so it straddles 0, eg, (-0.5, 0.5). Then add a random element.
    ret -= 0.5
    ret *= arg_gen()
    ret += 0.5
    return ret
