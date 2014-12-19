# -*- coding: utf-8 -*-
from django.db import models

from ...cadastros.models.produto import Produto
from .endereco import Endereco

class Saldo(models.Model):
    """
    Model para saldo de produtos
    """
    endereco = models.ForeignKey(Endereco, verbose_name='Endereco', blank=False, null=False, on_delete=models.PROTECT)
    produto  = models.ForeignKey(Produto , verbose_name='Produto' , blank=False, null=False, on_delete=models.PROTECT)
    quant    = models.DecimalField(verbose_name="Quantidade", blank=False, null=False, max_digits=19, decimal_places=4)

    def __unicode__(self):
        return self.endereco.codigo + ' - ' + self.produto.codigo + '::' + str(quant)

    class Meta:
        app_label = 'estoque'