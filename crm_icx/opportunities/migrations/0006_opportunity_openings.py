# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-15 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0005_auto_20171109_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='openings',
            field=models.IntegerField(default=0),
        ),
    ]
