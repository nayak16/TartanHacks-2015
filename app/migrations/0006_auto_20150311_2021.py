# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='cred',
            field=oauth2client.django_orm.CredentialsField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='spread',
            field=models.CharField(default='blank', max_length=200),
            preserve_default=False,
        ),
    ]
