# 🌱 BeMeta: online psychotherapy service
## Airtable to PostgreSQL sync script

### Short description

- Script was created for online psychotherapy service **Bemeta**
- It helps to upload data from Airtable to PostgreSQL (or basically almost any SQL Data Base)
- Also it includes Django web page with info about psychotherapists where transferred data are being used.

#### What I used:
- Django + Django ORM
- PostgreSQL + psycopg2 library
- Airtable API + requests library

# BeMeta

### Привет!

### Базовая информация по проекту:

Проект состоит из страницы со ссылками на терапевтов и страниц терапевтов, сверстанных по заданному шаблону.

### Развернуть и запустить проект:
- git clone https://github.com/atmay/Meta.git
- python3 -m venv -venv
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py collectstatic
- python manage.py runserver

### Скрипт для обновления базы данных здесь:
- Meta/update_data_from_airtable.py

Переменные окружения сохранены в отдельном файле .env (не залиты в git)

### Стек
Django, Django ORM, PostgreSQL + psycopg2, Airtable API + requests, CSS (flexbox)
