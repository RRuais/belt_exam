# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltexam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sender_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
