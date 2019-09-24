# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppMetaConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conf_name', models.CharField(max_length=64, verbose_name='\u914d\u7f6e\u540d\u79f0')),
                ('conf_value', models.TextField(verbose_name='\u914d\u7f6e\u503c')),
                ('remark', models.CharField(default=b'\xe6\x97\xa0', max_length=128, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'verbose_name': '\u914d\u7f6e\u8868',
                'verbose_name_plural': '\u914d\u7f6e\u8868',
            },
        ),
    ]
