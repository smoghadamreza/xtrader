# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2021-05-22 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='txid',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
