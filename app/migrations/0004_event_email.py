# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='email',
            field=models.EmailField(default=datetime.datetime(2015, 2, 7, 17, 25, 28, 264819, tzinfo=utc), max_length=75),
            preserve_default=False,
        ),
    ]
