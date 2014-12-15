# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='codigo',
            field=models.CharField(default=b'', max_length=15, verbose_name=b'C\xc3\xb3digo'),
            preserve_default=True,
        ),
    ]
