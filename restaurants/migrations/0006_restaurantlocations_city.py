# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 06:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_auto_20170725_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantlocations',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurants.City'),
            preserve_default=False,
        ),
    ]
