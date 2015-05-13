# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0008_auto_20150402_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Private_Access',
            new_name='Public_Access',
        ),
    ]
