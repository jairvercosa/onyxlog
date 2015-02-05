# -*- coding: utf-8 -*-
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField('auth.User', null=False)
    plantas = models.ManyToManyField(
            'cadastros.Planta',
            verbose_name='Platas de Operação',
            blank=False,
            null=True,
            related_name='perfil',
        )

    class Meta:
        app_label = 'acesso'
