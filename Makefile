all: edit

install:
	pip -r requirements.txt

edit:
	ipython qtconsole --pylab inline --quiet &
	vim demo.py
