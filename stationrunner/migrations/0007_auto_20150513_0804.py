# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stationrunner', '0006_station_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='c_owner',
            field=models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='channel',
            name='c_station',
            field=models.ForeignKey(default=b'', to='stationrunner.Station'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='station',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
