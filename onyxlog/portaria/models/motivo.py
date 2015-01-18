# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

class Motivo(models.Model):
    """
    Model do cadastro de motivos de visita
    """
    nome     = models.CharField(verbose_name=_('Nome'), max_length=60, blank=False, null=False)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = 'portaria'

class MotivoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """
    class Meta:
        model = Motivo
        fields = ('nome', )