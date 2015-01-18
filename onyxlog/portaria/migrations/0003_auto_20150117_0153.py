# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0002_auto_20150117_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentovisitante',
            name='veiculo',
            field=models.ForeignKey(related_name='ocupante', verbose_name=b'Ve\xc3\xadculo', blank=True, to='portaria.MovimentoVeiculo', null=True),
            preserve_default=True,
        ),
    ]
