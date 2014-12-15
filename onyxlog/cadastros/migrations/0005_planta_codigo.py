# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0004_planta'),
    ]

    operations = [
        migrations.AddField(
            model_name='planta',
            name='codigo',
            field=models.CharField(default=b'', max_length=10, verbose_name=b'C\xc3\xb3digo'),
            preserve_default=True,
        ),
    ]
