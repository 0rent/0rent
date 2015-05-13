# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0007_product_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Private_Access',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
