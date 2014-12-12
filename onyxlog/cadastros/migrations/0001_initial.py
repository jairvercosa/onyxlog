# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoProduto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=15, verbose_name='Code')),
                ('desc', models.CharField(max_length=60, verbose_name='Description')),
                ('desclong', models.TextField(null=True, verbose_name='Tall Description', blank=True)),
                ('revisao', models.CharField(max_length=10, verbose_name='Revision')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Group', blank=True, to='cadastros.GrupoProduto', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30, verbose_name='Nome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='produto',
            name='unidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Unit', blank=True, to='cadastros.Unidade', null=True),
            preserve_default=True,
        ),
    ]
