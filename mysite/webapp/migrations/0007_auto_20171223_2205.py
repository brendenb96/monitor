# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-23 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_miner_uptime'),
    ]

    operations = [
        migrations.AddField(
            model_name='miner',
            name='asic1',
            field=models.CharField(default='NONE', max_length=70),
        ),
        migrations.AddField(
            model_name='miner',
            name='asic2',
            field=models.CharField(default='NONE', max_length=70),
        ),
        migrations.AddField(
            model_name='miner',
            name='asic3',
            field=models.CharField(default='NONE', max_length=70),
        ),
    ]
