init:
	pip install -r requirements.txt

test:
	python2 /usr/bin/nosetests -s tests

install:
	rm -r ~/.local/lib/python2.7/site-packages/sample
	cp -r sample ~/.local/lib/python2.7/site-packages/
