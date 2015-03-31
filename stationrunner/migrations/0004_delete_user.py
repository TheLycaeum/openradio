# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0003_remove_station_owner'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
