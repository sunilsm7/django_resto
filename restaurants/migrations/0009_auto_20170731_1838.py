# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0008_auto_20170731_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantlocations',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.RestaurantCuisine'),
        ),
    ]
