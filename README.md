
# Jararaca

Sistema de gestão de eventos e check-in do Grupy-RN

[![codecov](https://codecov.io/gh/grupyrn/jararaca/graph/badge.svg?token=cjKiEu5oaZ)](https://codecov.io/gh/grupyrn/jararaca)
[![Testes](https://github.com/grupyrn/jararaca/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/grupyrn/jararaca/actions/workflows/django.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contribuindo

Contribuições são sempre bem-vindas!

Veja `contribuindo.md` para saber como começar.

## Rodando localmente

### Clone o projeto

```bash
  git clone https://github.com/grupyrn/jararaca
```

### Entre no diretório do projeto

```bash
  cd jararaca
```

Para instalar as dependências, será preciso usar o python 3.7.17

Para gerenciar o dependências, usaremos pip e o venv

### Crie um ambiente virtual
```bash
  python -m venv .venv
```

### Ative o ambiente virtual

No linux:

```bash
  source .venv/bin/activate
```

No windows:
```bash
  .venv/Scripts/Activate
```

### Instale as dependências do projeto
```bash
  pip install -r requirements-dev.txt
```

### Faça uma cópia do .env
```bash
  cp .env.sample .env
```

### Aplique as migrações:

```bash
  python manage.py migrate
```

### Crie um usuário administrador

```bash
  python manage.py createsuperuser
```

### Compile as traduções

```bash
  python manage.py compilemessages -f
```

### Execute o servidor

```bash
  python manage.py runserver
```

## Rodando os testes

Para rodar os testes, use:

```bash
  pytest .
```


## Stack utilizada

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](http://www.django-rest-framework.org/)
- [PyQRCode](https://pythonhosted.org/PyQRCode/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [SendGrid API](https://sendgrid.com/)
