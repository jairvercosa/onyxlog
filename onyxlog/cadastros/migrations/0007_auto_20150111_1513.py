# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_produto_validade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='validade',
            field=models.BooleanField(default=False, help_text=b'Indica se \xc3\xa9 obrigat\xc3\xb3ria a validade para emiss\xc3\xa3o da etiqueta.', verbose_name=b'Controla Validade'),
            preserve_default=True,
        ),
    ]
