# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='fornecedor',
            field=models.CharField(max_length=90, null=True, verbose_name=b'Fornecedor', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='codigo',
            field=models.CharField(max_length=15, verbose_name=b'C\xc3\xb3digo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='desc',
            field=models.CharField(max_length=60, verbose_name=b'Descri\xc3\xa7\xc3\xa3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='desclong',
            field=models.TextField(null=True, verbose_name=b'Descri\xc3\xa7\xc3\xa3o Grande', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Grupo', blank=True, to='cadastros.GrupoProduto', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='revisao',
            field=models.CharField(max_length=10, verbose_name=b'Revis\xc3\xa3o'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='produto',
            name='unidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Unidade de Medida', blank=True, to='cadastros.Unidade', null=True),
            preserve_default=True,
        ),
    ]
