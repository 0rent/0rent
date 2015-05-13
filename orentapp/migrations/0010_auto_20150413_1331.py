# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('orentapp', '0009_auto_20150402_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, to='auth.Group', serialize=False, parent_link=True, primary_key=True)),
                ('product', models.ForeignKey(to='orentapp.Product')),
            ],
            options={
            },
            bases=('auth.group',),
        ),
        migrations.RemoveField(
            model_name='product_access',
            name='Product',
        ),
        migrations.RemoveField(
            model_name='product_access',
            name='User',
        ),
        migrations.DeleteModel(
            name='Product_Access',
        ),
        migrations.AlterField(
            model_name='product',
            name='First_Owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
