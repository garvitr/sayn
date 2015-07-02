# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0007_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
