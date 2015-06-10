# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orentapp', '0019_auto_20150608_1959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ratio', models.DecimalField(decimal_places=2, max_digits=3)),
                ('product', models.ForeignKey(to='orentapp.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='first_owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='orentapp.Ownership'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='first_owner',
            field=models.ForeignKey(related_name='fowner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
