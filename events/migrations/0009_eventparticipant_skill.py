# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-13 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20170930_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparticipant',
            name='skill',
            field=models.TextField(blank=True, help_text='Skill'),
        ),
    ]
