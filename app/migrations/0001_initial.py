# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('money', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashString', models.CharField(max_length=200)),
                ('adminHashString', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=30)),
                ('admin', models.CharField(max_length=30)),
                ('total', models.DecimalField(max_digits=6, decimal_places=2)),
                ('goal', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contributor',
            name='event',
            field=models.ForeignKey(to='app.Event'),
            preserve_default=True,
        ),
    ]
