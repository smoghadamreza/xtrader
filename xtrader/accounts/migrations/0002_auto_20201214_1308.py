# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-12-14 12:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='expire',
            field=models.DateField(default=datetime.datetime(2020, 12, 24, 12, 7, 59, 281050, tzinfo=utc)),
        ),
    ]
