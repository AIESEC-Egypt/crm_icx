# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-07 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_remove_application_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_an_signed', models.DateTimeField(blank=True, null=True)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('date_realized', models.DateTimeField(blank=True, null=True)),
                ('experience_start_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='application',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='application',
            name='date_an_signed',
        ),
        migrations.RemoveField(
            model_name='application',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='application',
            name='date_realized',
        ),
        migrations.RemoveField(
            model_name='application',
            name='experience_start_date',
        ),
        migrations.RemoveField(
            model_name='application',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='application',
            name='timeline',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.Timeline'),
        ),
    ]
