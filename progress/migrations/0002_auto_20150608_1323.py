# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(max_length=20, choices=[('observer', 'Observer'), ('member', 'Member')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='society',
            field=models.ForeignKey(to='progress.Society'),
        ),
    ]
