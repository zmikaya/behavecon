# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('session', models.CharField(max_length=128)),
                ('group', models.IntegerField()),
                ('info_set', models.IntegerField()),
                ('state', models.CharField(max_length=128)),
                ('time', models.CharField(max_length=1000)),
                ('chat_room', models.CharField(max_length=128)),
                ('answers', models.CharField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('players', models.IntegerField()),
                ('active_players', models.CharField(max_length=10000)),
                ('stype', models.IntegerField(max_length=128)),
                ('date', models.CharField(max_length=128)),
                ('live', models.IntegerField()),
                ('groups', models.CharField(default=b'{"0": 0}', max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
