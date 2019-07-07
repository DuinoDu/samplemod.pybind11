install:
	python3.6 setup.py install

uninstall:
	python3.6 setup.py install --record install.log
	cat install.log | xargs rm -rf 
	rm install.log

test:
	python3.6 /usr/bin/nosetests -s tests

lint:
	pylint sample --reports=n

lintfull:
	pylint sample
