# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2021-05-02 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210429_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='income',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
