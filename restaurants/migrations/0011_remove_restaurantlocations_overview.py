# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 12:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0010_auto_20170804_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurantlocations',
            name='overview',
        ),
    ]
