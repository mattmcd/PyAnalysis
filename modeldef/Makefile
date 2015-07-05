all: java/ModelDefParser.class mdef/ModelDefParser.py

java/ModelDefParser.java: ModelDef.g4
	antlr4 -o java ModelDef.g4

java/ModelDefParser.class: java/ModelDefParser.java
	javac java/ModelDef*.java

mdef/ModelDefParser.py: ModelDef.g4
	antlr4 -o mdef -Dlanguage=Python2 ModelDef.g4
	touch mdef/__init__.py # Create mdef package

generatedFiles = {ModelDefLexer,ModelDefParser,ModelDefListener,ModelDefBaseListener}

clean:
	rm -f java/*
	rm -f mdef/*

grun= java org.antlr.v4.runtime.misc.TestRig
test: java/ModelDefParser.class
	$(grun) ModelDef modeldef -tokens ../test.txt

testpy: ModelDef.g4 program.py
	python program.py
