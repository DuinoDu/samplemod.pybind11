#python=python2.7
python=python3.6

build:
	$(python) setup.py build

upload:
	$(python) setup.py bdist_wheel upload -r hobot-local

clean:
	@rm -rf build dist src/*.egg-info

test:
	$(python) /usr/bin/nosetests -s tests --nologcapture

lint:
	pylint sample --reports=n

lintfull:
	pylint sample

install:
	$(python) setup.py install --user

uninstall:
	$(python) setup.py install --user --record install.log
	cat install.log | xargs rm -rf 
	@rm install.log
