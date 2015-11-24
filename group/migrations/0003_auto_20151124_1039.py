# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20150918_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='session',
            name='practice_questions',
        ),
    ]
