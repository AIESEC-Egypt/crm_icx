# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-06 13:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_application_date_an_signed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='updated',
        ),
    ]
