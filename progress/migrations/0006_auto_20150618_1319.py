# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0005_auto_20150618_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.IntegerField(choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed'), (3, 'Cancelled')]),
        ),
    ]
