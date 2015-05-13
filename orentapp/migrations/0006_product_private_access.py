# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0005_product_first_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Private_Access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
