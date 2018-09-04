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
pipenv install
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

Please feel free for submitting pull requests to us.
