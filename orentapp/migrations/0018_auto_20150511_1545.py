# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0017_product_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='private_group',
            field=models.OneToOneField(blank=True, to='auth.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='step',
            field=models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
    ]
