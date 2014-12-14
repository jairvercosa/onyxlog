# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_auto_20141213_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='desc',
            field=models.CharField(max_length=125, verbose_name=b'Descri\xc3\xa7\xc3\xa3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='desclong',
            field=models.TextField(null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o Completa', blank=True),
            preserve_default=True,
        ),
    ]
