# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-22 03:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('entity_type', models.CharField(choices=[('AI', 'AIESEC INTERNATIONAL'), ('RE', 'Regional'), ('MC', 'Members Committee'), ('LC', 'Local Committee'), ('XX', 'Type Unknown')], default='XX', max_length=2)),
                ('parent_committee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Committee')),
            ],
        ),
    ]