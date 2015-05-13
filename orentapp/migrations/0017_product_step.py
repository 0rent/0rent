# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orentapp', '0016_auto_20150422_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='step',
            field=models.DecimalField(max_digits=8, null=True, decimal_places=2),
            preserve_default=True,
        ),
    ]
