from django.test import TestCase

# Create your tests here.
# зарегистроваться в heroku

# скачать heroku CLI
# brew install heroku/brew/heroku

# heroku login
# в браузоре нажать логин

# heroku create
# в папке проекта

# проверить список удленных репозиториев
# git remote -v

# в requirements.txt указываем следующие зависимости
# gunicorn, whitenoise, python-decouple

# в settings.py добовляем стороку в midllwares:
# 'whitenoise.middleware.WhiteNoiseMiddleware',

# в корень проекта добавить Procfile
# web: gunicorn <название проекта>.wsgi

# создать базу данных в heroku/resourses-> add-ons-> heroku postgres

# добавить в heroku во вкладке settings->config vars все переменные окружения

# git push heroku main

# миграции
# heroku run python manage.py migrate

# heroku run python manage.py createsuperuser
