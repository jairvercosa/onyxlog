# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acesso', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='plantas',
            field=models.ManyToManyField(related_name='perfil', null=True, verbose_name=b'Platas de Opera\xc3\xa7\xc3\xa3o', to='cadastros.Planta'),
            preserve_default=True,
        ),
    ]
