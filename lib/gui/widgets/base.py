class BaseWidget:
  NULL_COORDS = 10000

  def draw(self):
    raise NotImplementedError()
  
  def reset(self):
    raise NotImplementedError()
  
  def disable(self):
    raise NotImplementedError()
  
  def enable(self):
    raise NotImplementedError()
