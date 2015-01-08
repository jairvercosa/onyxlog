# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_planta_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='validade',
            field=models.BooleanField(default=False, verbose_name=b'Controla Validade'),
            preserve_default=True,
        ),
    ]
