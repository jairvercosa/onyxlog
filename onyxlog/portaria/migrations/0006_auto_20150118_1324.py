# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portaria', '0005_auto_20150117_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='movimentovisitante',
            name='cpf',
            field=models.CharField(default=b'', help_text=b'Utilize apenas n\xc3\xbameros. N\xc3\xa3o utilize caracteres como ., - ou /', max_length=11, verbose_name=b'CPF'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimentovisitante',
            name='veiculo',
            field=models.ForeignKey(related_name='ocupantes', verbose_name=b'Ve\xc3\xadculo', blank=True, to='portaria.MovimentoVeiculo', null=True),
            preserve_default=True,
        ),
    ]
