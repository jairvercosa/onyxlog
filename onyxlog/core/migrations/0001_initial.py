# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=20, verbose_name=b'nome', db_index=True)),
                ('descricao', models.CharField(max_length=255, verbose_name=b'descri\xc3\xa7\xc3\xa3o')),
                ('valor', models.CharField(max_length=50, verbose_name=b'valor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
