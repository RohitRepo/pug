# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField()),
                ('device_id', models.CharField(max_length=16)),
                ('status', models.BooleanField(default=False)),
                ('connected', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name='devices', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField()),
                ('device_id', models.CharField(max_length=16)),
                ('status', models.BooleanField(default=False)),
                ('connected', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceValidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('device_id', models.CharField(max_length=16)),
                ('code', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
