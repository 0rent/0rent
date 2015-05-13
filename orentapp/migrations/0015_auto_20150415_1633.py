# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0014_product_private_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='private_group',
            field=models.ForeignKey(to='auth.Group', default=1),
            preserve_default=False,
        ),
    ]
