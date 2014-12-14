# -*- coding: utf-8 -*-
from django.db import models

from .grupo import GrupoProduto
from .unidade import Unidade

class Produto(models.Model):
	"""
	Model do cadastro de produtos
	"""
	codigo	   = models.CharField(verbose_name='Código', max_length=15, blank=False, null=False)
	fornecedor = models.CharField(verbose_name='Fornecedor', max_length=90, blank=True, null=True)
	desc	   = models.CharField(verbose_name='Descrição', max_length=125, blank=False, null=False)
	desclong   = models.TextField(verbose_name='Descrição Completa',blank=True,null=True)
	revisao	   = models.CharField(verbose_name='Revisão', max_length=10, blank=False, null=False)

	unidade	   = models.ForeignKey(Unidade, verbose_name='Unidade de Medida', blank=True, null=True, on_delete=models.PROTECT)
	grupo	   = models.ForeignKey(GrupoProduto, verbose_name='Grupo', blank=True, null=True, on_delete=models.PROTECT)

	def __unicode__(self):
		return self.codigo + ' - ' + self.desc

	class Meta:
		app_label = 'cadastros'

