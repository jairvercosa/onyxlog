# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

class Unidade(models.Model):
	"""
	Model do cadastro de unidades de media
	"""
	nome	 = models.CharField(verbose_name=_('Nome'), max_length=30, blank=False, null=False)

	def __unicode__(self):
		return self.nome

	class Meta:
		app_label = 'cadastros'

class UnidadeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """
    class Meta:
        model = Unidade
        fields = ('nome', )

