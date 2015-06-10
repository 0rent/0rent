# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0021_auto_20150610_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='first_owner',
        ),
    ]
