# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 06:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0002_auto_20161107_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resourcereq',
            fields=[
                ('reqid', models.IntegerField(db_column=b'ReqID', primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, db_column=b'Status', max_length=45, null=True)),
                ('etypeid', models.ForeignKey(blank=True, db_column=b'EtypeID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Equipment')),
                ('venueid', models.ForeignKey(blank=True, db_column=b'VenueID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Venue')),
            ],
            options={
                'db_table': 'resourcereq',
                'managed': True,
            },
        ),
    ]
