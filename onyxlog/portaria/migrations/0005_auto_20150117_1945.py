# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0004_auto_20150117_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='saida',
            field=models.DateField(null=True, verbose_name=b'Sa\xc3\xadda', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimento',
            name='saida_hora',
            field=models.TimeField(null=True, verbose_name=b'Hora Sa\xc3\xadda', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimentoveiculo',
            name='veiculo',
            field=models.CharField(help_text=b'Ex. Fiat P\xc3\xa1lio, Gol, Caminh\xc3\xa3o Scannia.', max_length=60, verbose_name=b'Ve\xc3\xadculo'),
            preserve_default=True,
        ),
    ]
