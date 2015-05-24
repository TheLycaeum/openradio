# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stationrunner.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stationrunner', '0009_auto_20150513_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('audio_file', models.FileField(upload_to=b'')),
                ('uploader', models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
