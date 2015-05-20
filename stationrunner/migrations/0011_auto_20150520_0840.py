# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('stationrunner', '0010_audiofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='channel',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='channel',
            name='station',
            field=models.ForeignKey(to='stationrunner.Station'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='station',
            name='address',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='station',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
