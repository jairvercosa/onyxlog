# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_planta_codigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(default=b'', max_length=10, verbose_name=b'C\xc3\xb3digo')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Planta', blank=True, to='cadastros.Planta', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
