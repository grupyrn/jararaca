# GruPy-RN Check-In API

GruPy-RN Event Check-in System

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

- Python 3
- [`pipenv`](https://pipenv.readthedocs.io/en/latest/)

### Installing

A step by step series of examples that tell you how to get a development env running

First of all, make a copy of `.env.sample` to `.env`

```
cp .env.sample .env
```

Install the dependencies

```
pipenv install sync --dev
```

### Running

Enter the `pipenv` virtual environment

```
pipenv shell
```

Apply the migrations

```
python manage.py migrate
```

Create admin user

```
python manage.py createsuperuser
```

Compile translations        

```
python manage.py compilemessages -f
```

And finally run the project

```
python manage.py runserver
```

Now you can open [http://localhost:8000](http://localhost:8000) in your browser

## Built With

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](http://www.django-rest-framework.org/)
- [PyQRCode](https://pythonhosted.org/PyQRCode/)
- [SendGrid](https://sendgrid.com/)

## Contributing


### Steps for Submitting Code

1. Fork the repository on GitHub.
2. Make your change.
3. Send a GitHub Pull Request to the main repository’s `master` branch. GitHub Pull Requests are the expected method of code collaboration on this project.

### Translate

1. Prepare message files for the desired language.

```
python manage.py makemessages --locale <language_code>
```

Example:

```
python manage.py makemessages --locale pt_BR
```

2. Translate the \*.po files inside each project application <app_name>/locale/<language_code>/LC_MESSAGES/

3. Compile messages

```
python manage.py compilemessages -f
```
