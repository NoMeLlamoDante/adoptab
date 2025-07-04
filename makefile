run:
	python3 manage.py runserver

mg:
	python3 manage.py makemigrations
	python3 manage.py migrate

csu:
	python3 manage.py createsuperuser

init:
	mv example.env .env
	mv adoptab/example.my.cnf