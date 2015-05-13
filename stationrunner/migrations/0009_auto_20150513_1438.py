# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0008_auto_20150513_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channel',
            old_name='c_frequency',
            new_name='frequency',
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='c_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='c_owner',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='channel',
            old_name='c_station',
            new_name='station',
        ),
    ]
