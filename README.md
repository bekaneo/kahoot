# DRF Kahoot Project

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/bekaneo/kahoot.git
$ cd kahoot
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.
Then install the dependencies:

# Postgres

To run application you need to create database and make migrations.

```sh
$ psql
$ CREATE DATABASE 'database_name'
$ \q
(env)$ python manage.py migrate
```

# .env

Then configure `.env_example` file and rename it to `.env`:

In order to test the kahoot app, create superuser.
```sh
(env)$ python manage.py createsuperuser
```
# Run the app
Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
