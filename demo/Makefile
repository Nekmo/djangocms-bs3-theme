.PHONY: all help translate test clean update collect rebuild

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: translate - calls the "makemessages" django command
translate:
	cd {{ project_name }} && django-admin.py makemessages -i "site-static/*" -a --no-location

# target: test - calls the "test" django command
test:
	django-admin.py test

# target: clean - remove all ".pyc" files
clean:
	django-admin.py clean_pyc

# target: update - install (and update) pip requirements
update:
	pip install -U -r requirements.txt

# target: collect - calls the "collectstatic" django command
collectstatic:
	django-admin.py collectstatic --noinput

# target: migrate - calls the "migrate" django command
migrate:
	django-admin.py migrate --noinput

# target: rebuild - clean, update, compass, collectstatic, then rebuild all data
rebuild: clean update collectstatic
	django-admin.py migrate
