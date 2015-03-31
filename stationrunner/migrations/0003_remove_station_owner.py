# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0002_auto_20150330_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='owner',
        ),
    ]
