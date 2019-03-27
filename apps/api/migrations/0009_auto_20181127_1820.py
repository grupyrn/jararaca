# Generated by Django 2.1.3 on 2018-11-27 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_auto_20180829_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(verbose_name='start time')),
                ('end', models.TimeField(verbose_name='end time')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('certificate_model', models.ImageField(null=True, upload_to='', verbose_name='certificate model')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.EventDay',
                                            verbose_name='event day')),
            ],
            options={
                'verbose_name': 'subevent',
                'verbose_name_plural': 'subevents',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='SubEventCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrance_date', models.DateTimeField(null=True, verbose_name='entrance date/time')),
                ('exit_date', models.DateTimeField(null=True, verbose_name='exit date/time')),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Attendee',
                                               verbose_name='attendee')),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.SubEvent',
                                               verbose_name='subevent')),
            ],
            options={
                'verbose_name': 'subevent check',
                'verbose_name_plural': 'subevent checks',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='certificate_model',
            field=models.ImageField(null=True, upload_to='', verbose_name='certificate model'),
        ),
    ]