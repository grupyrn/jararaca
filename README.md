# Jararaca

GruPy-RN Event and Check-in System

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

- Python 3.6+
- Node/NPM/Yarn

### Installing

A step by step series of examples that tell you how to get a development env running

First of all, make a copy of `.env.sample` to `.env`

```
cp .env.sample .env
```

Install the dependencies

```
pip install -r requirements.txt
```

Checkout [Jararaquinha](https://github.com/grupyrn/jararaquinha) submodule

```
git submodule init
git submodule update
```

Then, refer to [Jararaquinha's installation instructions](https://github.com/grupyrn/jararaquinha#installing).

### Running

Enter in your virtual environment.

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

Run the project

```
python manage.py runserver
```

And also run [Jararaquinha](https://github.com/grupyrn/jararaquinha) in another terminal

```
yarn start
```

Now you can open [http://localhost:8000](http://localhost:8000) in your browser

## Built With

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](http://www.django-rest-framework.org/)
- [PyQRCode](https://pythonhosted.org/PyQRCode/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [SendGrid API](https://sendgrid.com/)
- [React](https://reactjs.org/)

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
