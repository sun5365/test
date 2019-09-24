# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u5956\u9879\u540d\u79f0')),
                ('number', models.IntegerField(default=1, verbose_name='\u6bcf\u6b21\u4e2d\u5956\u4eba\u6570')),
                ('winRate', models.IntegerField(default=0, verbose_name='\u540d\u53551\u4e2d\u5956\u4eba\u6570')),
                ('winRate2', models.IntegerField(default=0, verbose_name='\u540d\u53552\u4e2d\u5956\u4eba\u6570')),
                ('times', models.IntegerField(default=1, verbose_name='\u62bd\u5956\u6b21\u6570')),
                ('prize', models.CharField(max_length=64, verbose_name='\u5956\u54c1')),
                ('status', models.IntegerField(default=1, verbose_name='\u72b6\u6001', choices=[(0, '\u672a\u6fc0\u6d3b'), (1, '\u5df2\u6fc0\u6d3b'), (2, '\u5df2\u7ed3\u675f')])),
                ('sequence', models.IntegerField(default=0, verbose_name='\u987a\u5e8f')),
                ('picture', models.ImageField(upload_to=b'award', verbose_name='\u5956\u54c1\u56fe\u7247')),
                ('compressed_picture', models.ImageField(upload_to=b'compressed_award', null=True, verbose_name='\u538b\u7f29\u56fe\u7247', blank=True)),
                ('compressed_image', models.TextField(null=True, blank=True)),
                ('image', models.TextField(null=True, blank=True)),
                ('needInput', models.BooleanField(default=False, verbose_name='\u662f\u5426\u73b0\u573a\u8f93\u5165\u5956\u54c1')),
                ('changeWinRateInPlace', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53ef\u4ee5\u73b0\u573a\u66f4\u6539\u4e2d\u5956\u4eba\u6570')),
                ('ignoreAnimation', models.BooleanField(default=True, verbose_name='\u662f\u5426\u8df3\u8fc7\u62bd\u5956\u52a8\u753b')),
                ('everyoneCanDraw', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6240\u6709\u4eba\u90fd\u53ef\u4ee5\u62bd\u5956')),
                ('isAddToExclusion', models.BooleanField(default=False, verbose_name='\u4e2d\u5956\u4eba\u5458\u662f\u5426\u52a0\u5230\u6392\u9664\u540d\u5355')),
                ('takeInScene', models.BooleanField(default=False, verbose_name='\u662f\u5426\u73b0\u573a\u9886\u5956')),
            ],
            options={
                'verbose_name': '\u5956\u9879',
                'verbose_name_plural': '\u5956\u9879',
            },
        ),
        migrations.CreateModel(
            name='Exclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('award', models.ForeignKey(verbose_name='\u5956\u9879', to='lottery.Award')),
                ('staff', models.ForeignKey(verbose_name='\u4e2d\u5956\u8005\u540d\u79f0', to='staff.Staff')),
            ],
            options={
                'verbose_name': '\u6392\u9664\u540d\u5355',
                'verbose_name_plural': '\u6392\u9664\u540d\u5355',
            },
        ),
        migrations.CreateModel(
            name='ExclusionForAll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff', models.ForeignKey(verbose_name='\u4e2d\u5956\u8005\u540d\u79f0', to='staff.Staff')),
            ],
            options={
                'verbose_name': '\u6392\u9664\u540d\u5355ForAll',
                'verbose_name_plural': '\u6392\u9664\u540d\u5355ForAll',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='\u62bd\u5956\u8ba1\u5212\u540d\u79f0')),
                ('description', models.CharField(max_length=1024, verbose_name='\u62bd\u5956\u8ba1\u5212\u63cf\u8ff0')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(0, '\u672a\u6fc0\u6d3b'), (1, '\u5df2\u6fc0\u6d3b')])),
            ],
            options={
                'verbose_name': '\u62bd\u5956\u8ba1\u5212',
                'verbose_name_plural': '\u62bd\u5956\u8ba1\u5212',
            },
        ),
        migrations.CreateModel(
            name='WheelItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=16, verbose_name='\u6807\u9898')),
            ],
            options={
                'verbose_name': '\u5927\u8f6c\u76d8\u9879',
                'verbose_name_plural': '\u5927\u8f6c\u76d8\u9879',
            },
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remark', models.CharField(max_length=256, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('award', models.ForeignKey(verbose_name='\u5956\u9879', to='lottery.Award')),
                ('staff', models.ForeignKey(verbose_name='\u4e2d\u5956\u8005\u540d\u79f0', to='staff.Staff')),
            ],
            options={
                'verbose_name': '\u4e2d\u5956\u4eba\u5458',
                'verbose_name_plural': '\u4e2d\u5956\u4eba\u5458',
            },
        ),
        migrations.AddField(
            model_name='award',
            name='plan',
            field=models.ForeignKey(verbose_name='\u62bd\u5956\u8ba1\u5212', to='lottery.Plan'),
        ),
        migrations.AddField(
            model_name='award',
            name='staffList',
            field=models.ForeignKey(related_name='staff_list', on_delete=django.db.models.deletion.PROTECT, verbose_name='\u5173\u8054\u540d\u53551', to='staff.StaffList'),
        ),
        migrations.AddField(
            model_name='award',
            name='staffList2',
            field=models.ForeignKey(related_name='staff_list_2', on_delete=django.db.models.deletion.PROTECT, verbose_name='\u5173\u8054\u540d\u53552', to='staff.StaffList', null=True),
        ),
    ]
