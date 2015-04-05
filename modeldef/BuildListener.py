from ModelDefListener import ModelDefListener
from ModelDefParser import ModelDefParser
# Add a listener to report values found
class BuildListener(ModelDefListener):
    def __init__(self):
        self.theStack = [];  # Execution stack
        self.map = {};       # Variable map

    # override default listener behavior
    def exitId(self,ctx) : 
        #LOGGER.info( "Exiting Id" );
        id = ctx.ID().getText();
        # LOGGER.info( "  Pushing value of " + id + " to stack" );
        if ( self.map.has_key(id) ) : 
            self.theStack.append( self.map[id] );

    def exitAssign(self, ctx) : 
        self.map[ctx.ID().getText()] = self.theStack.pop();


    def exitInt(self,ctx) :
        # LOGGER.info( "Exiting Int" );
        self.theStack.append( int( ctx.INT().getText() ));


    def exitPrint(self, ctx) :
        #LOGGER.info( "Exiting Print" );
        if ( not (len(self.theStack) < 1) ) :
            print self.theStack.pop();

    def exitClear(self,ctx) :
        # LOGGER.info("Exiting Clear");
        self.theStack = [];
        self.map = {};

    def exitAddSub(self,ctx) :
        #LOGGER.info( "Exiting AddSub" );
        b = self.theStack.pop();
        a = self.theStack.pop();
        if (ctx.op.type == ModelDefParser.ADD ) :
            result = a+b;
        else:
            result = a-b;
        self.theStack.append( result );

    def exitMulDiv(self,ctx) :
        # LOGGER.info( "Exiting MulDiv" );
        b = self.theStack.pop();
        a = self.theStack.pop();
        if (ctx.op.type == ModelDefParser.MUL) :
            result = a*b;
        else :
            result = a/b; # Integer divisiion?
        self.theStack.append( result );

