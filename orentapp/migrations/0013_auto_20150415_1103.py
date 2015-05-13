# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0012_auto_20150413_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='public_access',
            new_name='is_public',
        ),
        migrations.RenameField(
            model_name='profil',
            old_name='Balance',
            new_name='balance',
        ),
        migrations.RenameField(
            model_name='profil',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='use',
            old_name='Date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='use',
            old_name='Product',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='use',
            old_name='User',
            new_name='user',
        ),
    ]
