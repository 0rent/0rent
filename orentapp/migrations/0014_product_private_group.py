# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('orentapp', '0013_auto_20150415_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='private_group',
            field=models.ForeignKey(to='auth.Group', null=True),
            preserve_default=True,
        ),
    ]
