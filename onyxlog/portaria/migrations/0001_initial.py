# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'E', help_text=b'Tipo da movimenta\xc3\xa7\xc3\xa3o', max_length=1, verbose_name=b'Tipo')),
                ('data', models.DateTimeField()),
                ('liberado_por', models.CharField(help_text=b'Usu\xc3\xa1rio que liberou a entrada.', max_length=80, null=True, verbose_name=b'Liberado por', blank=True)),
                ('obs', models.TextField(null=True, verbose_name=b'Obs', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MovimentoVeiculo',
            fields=[
                ('movimento_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portaria.Movimento')),
                ('veiculo', models.CharField(help_text=b'Ex. Fiat P\xc3\xa1lio, Gol, Caminh\xc3\xa3o Scannea.', max_length=60, verbose_name=b'Ve\xc3\xadculo')),
                ('placa', models.CharField(max_length=7, verbose_name=b'Placa')),
                ('cor', models.CharField(help_text=b'Descreva a cor do ve\xc3\xadculo.', max_length=30, verbose_name=b'Cor')),
                ('nota', models.CharField(help_text=b'Nota fiscal que est\xc3\xa1 sendo entregue.', max_length=20, null=True, verbose_name=b'Nota Fiscal', blank=True)),
                ('fornecedor', models.CharField(max_length=80, null=True, verbose_name=b'Fornecedor', blank=True)),
            ],
            options={
            },
            bases=('portaria.movimento',),
        ),
        migrations.CreateModel(
            name='MovimentoVisitante',
            fields=[
                ('movimento_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='portaria.Movimento')),
                ('cpf', models.CharField(max_length=11, null=True, verbose_name=b'CPF', blank=True)),
                ('nome', models.CharField(max_length=100, verbose_name=b'Nome')),
                ('empresa', models.CharField(max_length=60, null=True, verbose_name=b'Empresa', blank=True)),
                ('veiculo', models.ForeignKey(related_name='ocupante', verbose_name=b'Ve\xc3\xadculo', to='portaria.MovimentoVeiculo')),
            ],
            options={
            },
            bases=('portaria.movimento',),
        ),
    ]
