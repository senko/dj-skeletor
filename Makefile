MANAGE=python manage.py
SETTINGS=--settings=project.settings.test

.PHONY: all test coverage clean requirements update \
	ensure_virtualenv reqs/dev reqs/test reqs/prod dev-setup

all: coverage

test:
	$(MANAGE) test --where=. $(SETTINGS) --with-xunit

coverage:
	$(MANAGE) test --where=. $(SETTINGS) \
		--with-xcoverage --with-xunit --cover-html  --cover-erase

clean:
	rm -rf .coverage cover nosetests.xml coverage.xml
	rm -rf skeletor/static/CACHE
	find . -name '*.pyc' -exec rm '{}' ';'

ensure_virtualenv:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "Please run me inside virtualenv.";  \
		exit 1; \
	fi

reqs/dev: ensure_virtualenv
	pip install -r requirements/dev.txt

reqs/test: ensure_virtualenv
	pip install -r requirements/test.txt

reqs/prod: ensure_virtualenv
	pip install -r requirements/prod.txt

dev-setup: ensure_virtualenv
	$(MAKE) reqs/dev
	if [ ! -f project/settings/local.py ]; then \
		echo 'from .dev import *' > project/settings/local.py; \
	fi
	$(MANAGE) syncdb --all
	$(MANAGE) migrate --fake

update: ensure_virtualenv
	$(MAKE) reqs/prod
	$(MAKE) clean
	$(MANAGE) syncdb
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput
