# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0012_auto_20150522_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='tags',
            field=models.ManyToManyField(to='stationrunner.Tag', null=True),
            preserve_default=True,
        ),
    ]
