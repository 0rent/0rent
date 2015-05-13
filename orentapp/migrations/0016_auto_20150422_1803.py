# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0015_auto_20150415_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='private_group',
            field=models.OneToOneField(to='auth.Group'),
            preserve_default=True,
        ),
    ]
