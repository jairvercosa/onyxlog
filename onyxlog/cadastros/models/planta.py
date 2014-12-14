# -*- coding: utf-8 -*-
from django.db import models

class Planta(models.Model):
    """
    Model do cadastro de plantas de operação
    """
    nome = models.CharField(verbose_name='Nome', max_length=60, blank=False, null=False)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'cadastros'