# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='payment',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='practice_questions',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
