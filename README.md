# Meta

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
