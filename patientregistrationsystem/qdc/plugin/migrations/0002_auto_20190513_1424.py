# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-13 17:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plugin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='randomforests',
            options={'permissions': (('can_send_data_to_plugin', 'Can send data to plugin'),)},
        ),
    ]
