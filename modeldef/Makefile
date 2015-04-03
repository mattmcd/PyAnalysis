all: ModelDef.class ModelDefParser.py

ModelDefParser.java: ModelDef.g4
	antlr4 ModelDef.g4

ModelDef.class: ModelDefParser.java
	javac ModelDef*.java

ModelDefParser.py: ModelDef.g4
	antlr4 -Dlanguage=Python2 ModelDef.g4

generatedFiles = ModelDefLexer.* ModelDefParser.* ModelDefListener.* ModelDefBaseListener.*

clean:
	rm -f $(generatedFiles) *.class *.tokens

grun= java org.antlr.v4.runtime.misc.TestRig
test: ModelDef.class
	$(grun) ModelDef modeldef -tokens test.txt

testpy: ModelDef.g4 program.py
	python program.py
