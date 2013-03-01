MANAGE=python manage.py
SETTINGS=--settings=skeletor.settings.test

.PHONY: all test coverage clean requirements

all: coverage

test:
	$(MANAGE) test --where=. $(SETTINGS)

coverage:
	$(MANAGE) test --where=. $(SETTINGS) \
		--with-xcoverage --with-xunit --cover-html  --cover-erase

clean:
	rm -rf .coverage cover nosetests.xml coverage.xml
	find . -name '*.pyc' -exec rm '{}' ';'

requirements:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You should probably install stuff in virtualenv instead."; \
	else \
		pip install -r requirements.txt; \
	fi
