# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0006_auto_20150118_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='motivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Motivo da Visita', to='portaria.Motivo', null=True),
            preserve_default=True,
        ),
    ]
