# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_userprofile'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookid', models.ForeignKey(db_column='idBookRequest', on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Bookrequest')),
                ('facultyid', models.ForeignKey(db_column='FacultyID', on_delete=django.db.models.deletion.DO_NOTHING, to='log.Faculty')),
            ],
            options={
                'db_table': 'faculty_book',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StudentBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookid', models.ForeignKey(db_column='idBookRequest', on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Bookrequest')),
                ('usn', models.ForeignKey(db_column='USN', on_delete=django.db.models.deletion.DO_NOTHING, to='log.Student')),
            ],
            options={
                'db_table': 'student_book',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VenueEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
                ('etypeid', models.ForeignKey(db_column='EtypeID', on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Equipment')),
                ('venueid', models.ForeignKey(db_column='VenueID', on_delete=django.db.models.deletion.DO_NOTHING, to='rooms.Venue')),
            ],
            options={
                'db_table': 'venue_equipment',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='venueequipment',
            unique_together=set([('venueid', 'etypeid')]),
        ),
        migrations.AlterUniqueTogether(
            name='studentbook',
            unique_together=set([('usn', 'bookid')]),
        ),
        migrations.AlterUniqueTogether(
            name='facultybook',
            unique_together=set([('facultyid', 'bookid')]),
        ),
    ]
