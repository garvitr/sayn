# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('position', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('date_of_birth', models.DateField()),
                ('role', models.CharField(max_length=20)),
                ('contact_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Contact number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('nominated_on', models.DateField()),
                ('nominated_through', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('contact_firstname', models.CharField(max_length=30)),
                ('contact_lastname', models.CharField(max_length=30)),
                ('contact_position', models.CharField(max_length=100)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='society',
            field=models.OneToOneField(to='progress.Society'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions'),
        ),
    ]
