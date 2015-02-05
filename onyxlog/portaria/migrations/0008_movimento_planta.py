# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_auto_20150111_1513'),
        ('portaria', '0007_movimento_motivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='planta',
            field=models.ForeignKey(default=1, verbose_name=b'Planta de Opera\xc3\xa7\xc3\xa3o', to='cadastros.Planta'),
            preserve_default=True,
        ),
    ]
