# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-12-14 12:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201214_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='expire',
            field=models.DateField(default=datetime.datetime(2020, 12, 24, 12, 8, 7, 985495, tzinfo=utc)),
        ),
    ]
