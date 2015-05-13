# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0011_auto_20150413_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Cost',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='First_Owner',
            new_name='first_owner',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Post_Date',
            new_name='post_date',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Public_Access',
            new_name='public_access',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Update_Date',
            new_name='update_date',
        ),
    ]
