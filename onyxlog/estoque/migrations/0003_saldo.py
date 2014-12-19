# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_planta_codigo'),
        ('estoque', '0002_auto_20141214_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saldo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quant', models.DecimalField(verbose_name=b'Quantidade', max_digits=19, decimal_places=4)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Endereco', to='estoque.Endereco')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Produto', to='cadastros.Produto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
