# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0003_auto_20150117_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimento',
            name='data',
        ),
        migrations.RemoveField(
            model_name='movimento',
            name='tipo',
        ),
        migrations.AddField(
            model_name='movimento',
            name='codigo',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'C\xc3\xb3digo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movimento',
            name='entrada',
            field=models.DateField(default=datetime.datetime(2015, 1, 17, 14, 26, 15, 191509, tzinfo=utc), verbose_name=b'Entrada', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movimento',
            name='entrada_hora',
            field=models.TimeField(null=True, verbose_name=b'Hora Entrada', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movimento',
            name='saida',
            field=models.DateTimeField(null=True, verbose_name=b'Sa\xc3\xadda', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movimento',
            name='saida_hora',
            field=models.DateTimeField(null=True, verbose_name=b'Hora Sa\xc3\xadda', blank=True),
            preserve_default=True,
        ),
    ]
