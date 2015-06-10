# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def move_first_owner(apps, schema_editor):
        Product = apps.get_model("orentapp", "Product")
        Ownership = apps.get_model("orentapp", "Ownership")
        for product in Product.objects.all():
            ownership = Ownership(product=product, user=product.first_owner,
                                  ratio=1)
            ownership.save()

    dependencies = [
        ('orentapp', '0020_auto_20150610_0927'),
    ]

    operations = [
        migrations.RunPython(move_first_owner),
    ]
