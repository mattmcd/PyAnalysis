all: edit

install:
	pip install -r requirements.txt

edit:
	ipython qtconsole --pylab inline --quiet > /dev/null 2>&1 &
	vim demo.py
