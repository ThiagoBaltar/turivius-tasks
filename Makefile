#!/bin/bash
.PHONY: default
.SILENT:


default:
	echo "Run make install or make start"

install: _local_env_create build start migrate loaddata stop
	echo "Done."

uninstall: _local_env_create
	docker compose down --remove-orphans --volumes --rmi all
	-docker images -q -f dangling=true | xargs docker rmi -f
	rm local.env || true

reinstall: uninstall install
	echo "Done."

start:
	docker compose up -d --remove-orphans

stop:
	docker compose rm -s -f -v

restart:
	docker compose rm -s -f django
	docker compose up -d django

watch:
	docker compose watch django

# ======================================================================
# ======================================================================
# ======================================================================
build:
	docker compose build

build-force: clean-layers
	docker compose build --force-rm --no-cache --pull

clean-layers:
	-docker images -q -f dangling=true | xargs docker rmi -f

# ======================================================================
# ======================================================================
# ======================================================================
pip-install:
	docker compose run --rm django-builder pipenv install $(lib)
	docker compose build
	make restart

shell:
	docker compose exec django bash

shell-root:
	docker compose exec -u root django bash

shell-builder:
	docker compose run --rm django-builder bash

runserver:
	docker compose exec django python manage.py runserver 0:8000

python:
	docker compose exec django python manage.py shell

migrate:
	docker compose run --rm django-builder python manage.py migrate --noinput --traceback --force-color

makemigrations:
	docker compose run --rm django-builder python manage.py makemigrations

logs:
	docker compose logs --follow

django-logs:
	docker compose logs django --follow

loaddata:
	docker compose run --rm django python manage.py loaddata user_admin

drop_db:
	docker-compose run --rm django python manage.py flush --noinput

restart_db: drop_db migrate
	echo "Done."

_local_env_create:
	-cp -n .env.sample .env.local
