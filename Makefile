.PHONY: run-server
run-server:
	poetry run python3 src/manage.py runserver

.PHONY: migrations
migrations:
	poetry run python3 src/manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python3 src/manage.py migrate

.PHONY: install
install:
	poetry install

.PHONY: superuser
superuser:
	poetry run python3 src/manage.py createsuperuser

.PHONY: update
update: install makemigrations migrate ;runserver

.PHONY: update
collectstatic:
	poetry run python3 src/manage.py collectstatic