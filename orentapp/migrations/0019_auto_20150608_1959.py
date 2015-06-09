# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('orentapp', '0018_auto_20150511_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privategroup',
            name='group_ptr',
        ),
        migrations.RemoveField(
            model_name='privategroup',
            name='product',
        ),
        migrations.DeleteModel(
            name='PrivateGroup',
        ),
        migrations.AlterField(
            model_name='profil',
            name='balance',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=8),
            preserve_default=True,
        ),
    ]
