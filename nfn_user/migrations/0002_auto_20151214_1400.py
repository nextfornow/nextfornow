# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfn_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c_owner',
            name='website',
            field=models.URLField(max_length=500, verbose_name='Website'),
        ),
    ]
