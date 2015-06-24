# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0004_auto_20150611_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed'), (3, 'Completed')]),
        ),
    ]
