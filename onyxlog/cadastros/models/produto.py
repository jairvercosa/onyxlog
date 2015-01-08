# -*- coding: utf-8 -*-
from django.db import models
from rest_framework import serializers
from .grupo import GrupoProduto, GrupoProdutoSerializer
from .unidade import Unidade, UnidadeSerializer

class Produto(models.Model):
    """
    Model do cadastro de produtos
    """
    codigo	   = models.CharField(verbose_name='Código', max_length=15, blank=False, null=False)
    fornecedor = models.CharField(verbose_name='Fornecedor', max_length=90, blank=True, null=True)
    desc	   = models.CharField(verbose_name='Descrição', max_length=125, blank=False, null=False)
    desclong   = models.TextField(verbose_name='Descrição Completa',blank=True,null=True)
    revisao	   = models.CharField(verbose_name='Revisão', max_length=10, blank=False, null=False)
    validade   = models.BooleanField(
        verbose_name='Controla Validade', 
        blank=True, 
        null=False, 
        default=False,
        help_text='Indica se é obrigatória a validade para emissão da etiqueta.',
    )

    unidade	   = models.ForeignKey(Unidade, verbose_name='Unidade de Medida', blank=True, null=True, on_delete=models.PROTECT)
    grupo	   = models.ForeignKey(GrupoProduto, verbose_name='Grupo', blank=True, null=True, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.codigo + ' - ' + self.desc

    class Meta:
        app_label = 'cadastros'

class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """
    unidade = UnidadeSerializer()
    grupo = GrupoProdutoSerializer()

    class Meta:
        model = Produto
        fields = ('codigo', 'fornecedor', 'desc', 'desclong', 'revisao', 'unidade', 'grupo', 'validade', )
