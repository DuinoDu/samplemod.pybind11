init:
	pip3 install -r requirements.txt

test:
	python3.6 /usr/bin/nosetests -s tests

lint:
	pylint sample --reports=n

lintfull:
	pylint sample
