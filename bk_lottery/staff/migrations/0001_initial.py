# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16, verbose_name='\u82f1\u6587\u540d')),
                ('chineseName', models.CharField(max_length=64, null=True, verbose_name='\u4e2d\u6587\u540d', blank=True)),
                ('department', models.CharField(max_length=64, null=True, verbose_name='\u90e8\u95e8', blank=True)),
                ('phone', models.CharField(max_length=16, null=True, verbose_name='\u7535\u8bdd', blank=True)),
                ('avatar', models.CharField(max_length=256, null=True, verbose_name='\u5934\u50cf', blank=True)),
                ('is_absent', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f3a\u5e2d')),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='StaffList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name='\u540d\u5355\u540d\u79f0')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u540d\u5355',
                'verbose_name_plural': '\u540d\u5355',
            },
        ),
        migrations.AddField(
            model_name='staff',
            name='staffList',
            field=models.ForeignKey(verbose_name='\u540d\u5355\u540d\u79f0', to='staff.StaffList'),
        ),
    ]
