# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0003_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_on',
            field=models.DateField(),
        ),
    ]
