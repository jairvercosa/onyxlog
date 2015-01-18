# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimento',
            name='tipo',
            field=models.CharField(default=b'E', help_text=b'Tipo da movimenta\xc3\xa7\xc3\xa3o', max_length=1, verbose_name=b'Tipo', choices=[(b'E', b'Entrada'), (b'S', b'Sa\xc3\xadda')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimentovisitante',
            name='cpf',
            field=models.CharField(default=b'', max_length=11, verbose_name=b'CPF'),
            preserve_default=True,
        ),
    ]
