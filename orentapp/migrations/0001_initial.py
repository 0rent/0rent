# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('Name', models.CharField(max_length=64)),
                ('Description', models.CharField(max_length=512)),
                ('Cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('Post_Date', models.DateField(auto_now_add=True)),
                ('Update_Date', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
