# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-17 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BugIdMap',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('messageid', models.CharField(max_length=500)),
            ],
        ),
    ]
