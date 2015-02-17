# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_event_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(default='A Friend', max_length=30),
            preserve_default=False,
        ),
    ]
