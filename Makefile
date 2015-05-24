all: edit

install:
	pip install -r requirements.txt

ipython:
	ipython qtconsole --pylab inline --quiet > /dev/null 2>&1 &
	vim demo.py

rodeo:
	rodeo . 
