# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20170715_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='other_center',
            field=models.CharField(blank=True, help_text='Center name if not available above', max_length=50),
        ),
    ]