# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-07 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190306_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecoed',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '忘记')], max_length=10, verbose_name='类型'),
        ),
    ]