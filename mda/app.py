class componentFactory(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        
    def addComponent( self, name, ctor):
        self.dispatcher[name] = ctor

    def getComponent(self, name, **kwargs ):
        try:
            f = self.dispatcher[name];
        except KeyError:
            raise ValueError('Invalid value')
        return f(**kwargs)
