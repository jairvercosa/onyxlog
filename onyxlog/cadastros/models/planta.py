# -*- coding: utf-8 -*-
from django.db import models
from rest_framework import serializers

class Planta(models.Model):
    """
    Model do cadastro de plantas de operação
    """
    codigo = models.CharField(verbose_name='Código', max_length=10, blank=False, null=False, default='')
    nome = models.CharField(verbose_name='Nome', max_length=60, blank=False, null=False)

    def __unicode__(self):
        return self.codigo + '-' + self.nome

    class Meta:
        app_label = 'cadastros'

class PlantaSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """
    class Meta:
        model = Planta
        fields = ('codigo', 'nome', )