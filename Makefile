install:
	python3.6 setup.py install --user

uninstall:
	python3.6 setup.py install --user --record install.log
	cat install.log | xargs rm -rf 
	@rm install.log

clean:
	@rm -rf build dist src/*.egg-info

test:
	python3.6 /usr/bin/nosetests -s tests

lint:
	pylint sample --reports=n

lintfull:
	pylint sample
