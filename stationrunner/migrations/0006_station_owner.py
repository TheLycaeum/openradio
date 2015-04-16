# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stationrunner', '0005_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='owner',
            field=models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
