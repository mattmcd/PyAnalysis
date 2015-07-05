from antlr4 import *
from mdef.ModelDefLexer import ModelDefLexer
from mdef.ModelDefParser import ModelDefParser
#from EvalListener import EvalListener

def main(input_str):

    # input = "a=1\na\nclear\na\na=3\na\nb=2+a\nb+a\n"

    print input_str
    chars = InputStream.InputStream(input_str);
    lexer = ModelDefLexer(chars);
    tokens = CommonTokenStream(lexer);
    parser = ModelDefParser(tokens);
    tree = parser.modeldef();

    print tree
    # Actually do the walking
    #evaluator = EvalListener();
    #walker = ParseTreeWalker();
    #walker.walk(evaluator, tree);

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    else:
        infile = 'test.txt'
    f = open(infile, 'r')
    input_str = [x for x in f.readlines()]
    f.close()

    map(main, input_str)
