run:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

restartdb:
	dropdb soloeng_db
	createdb soloeng_db
	python3 manage.py makemigrations account
	python3 manage.py migrate
	python3 manage.py createsuperuser

