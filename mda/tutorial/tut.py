def times2(x):
    return x*2

class Foo(object):
  def __init__(self,a,b):
    self.A = a
    self.B = b

class Bar(object):
  def __init__(self, x, y):
    self.X = x
    self.Y = y

def foobarFactory(name, **kwargs):
  dispatcher = {'Foo': Foo, 'Bar' : Bar};
  try:
    f = dispatcher[name]
    return f( **kwargs )
  except KeyError:
    raise ValueError('Invalid input')
