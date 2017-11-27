# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-20 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_auto_20171109_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='date_application_survey_filled',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timeline',
            name='date_application_survey_reviewed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timeline',
            name='date_application_survey_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timeline',
            name='state_application_survey_filled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timeline',
            name='state_application_survey_reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timeline',
            name='state_application_survey_sent',
            field=models.BooleanField(default=False),
        ),
    ]
