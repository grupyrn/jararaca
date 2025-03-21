# Jararaca

Sistema de gestão de eventos e check-in do Grupy-RN

[![codecov](https://codecov.io/gh/grupyrn/jararaca/graph/badge.svg?token=cjKiEu5oaZ)](https://codecov.io/gh/grupyrn/jararaca)

## Iniciando

Estas instruções irão ajudá-lo a obter uma cópia do projeto em funcionamento em sua máquina local para fins de desenvolvimento e teste.

### Pré-requisitos

O que você precisa instalar para rodar o software e como instalá-los:

- Python 3.7.17

### Instalando

Uma série de passos que explicam como configurar o ambiente de desenvolvimento.

Primeiramente, faça uma cópia do arquivo `.env.sample` para `.env`:

```
cp .env.sample .env
```

### Crie um ambiente virtual

```
python -m venv venv
```

Instale as dependências:

```
pip install -r requirements.txt
```

### Executando

Entre no seu ambiente virtual:

```
source venv/bin/activate
```

Aplique as migrações:

```
python manage.py migrate
```

Crie um usuário administrador:

```
python manage.py createsuperuser
```

Compile as traduções:

```
python manage.py compilemessages -f
```

Execute o projeto:

```
python manage.py runserver
```

Agora você pode acessar [http://localhost:8000](http://localhost:8000) no seu navegador.

## Construído com

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](http://www.django-rest-framework.org/)
- [PyQRCode](https://pythonhosted.org/PyQRCode/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [SendGrid API](https://sendgrid.com/)
- [React](https://reactjs.org/)

## Contribuindo

### Passos para submeter Código

1. Faça um fork do repositório no GitHub.
2. Faça suas alterações.
3. Envie um Pull Request no GitHub para a branch `master` do repositório principal. Os Pull Requests no GitHub são o método esperado para colaboração neste projeto.

### Traduzindo

1. Prepare os arquivos de mensagens para o idioma desejado:

```
python manage.py makemessages --locale <código_do_idioma>
```

Exemplo:

```
python manage.py makemessages --locale pt_BR
```

2. Traduza os arquivos \*.po dentro de cada aplicação do projeto em `<nome_do_app>/locale/<código_do_idioma>/LC_MESSAGES/`

3. Compile as mensagens:

```
python manage.py compilemessages -f
```
