# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-17 13:44
from __future__ import unicode_literals

from django.db import migrations, models


def map_translation(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    SignFeedback = apps.get_model('feedback', 'SignFeedback')
    for fb in SignFeedback.objects.all():
        fb.name = fb.translation.translation.text
        fb.save()


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20170917_2344'),
    ]

    operations = [
        migrations.RunPython(map_translation),
    ]
