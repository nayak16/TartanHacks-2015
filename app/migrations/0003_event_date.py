# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_event_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 2, 7, 16, 20, 1, 535892, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
