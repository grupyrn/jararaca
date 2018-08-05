import argparse

from django.core.management.base import BaseCommand, CommandError

from api.certificate import generate_certificate


class Command(BaseCommand):
    help = 'Generate a certificate for a determinate user'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
        parser.add_argument('--cpf', type=int, default=None)
        parser.add_argument('output', type=argparse.FileType('wb'))

    def handle(self, *args, **options):

        data = generate_certificate(options['name'], cpf=options['cpf'])
        options['output'].write(data.read())
        options['output'].close()
        self.stdout.write(self.style.SUCCESS('Successfully generated certificate for "%s"' % options['name']))