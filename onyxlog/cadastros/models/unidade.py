# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Unidade(models.Model):
	"""
	Model do cadastro de unidades de media
	"""
	nome	 = models.CharField(verbose_name=_('Nome'), max_length=30, blank=False, null=False)

	def __unicode__(self):
		return self.nome

	class Meta:
		app_label = 'cadastros'

