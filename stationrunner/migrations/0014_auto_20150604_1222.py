# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0013_auto_20150603_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='tags',
            field=models.ManyToManyField(to='stationrunner.Tag'),
            preserve_default=True,
        ),
    ]
