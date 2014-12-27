# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from ...cadastros.models.produto import Produto, ProdutoSerializer
from .endereco import Endereco, EnderecoSerializer

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

class SaldoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador do saldo de produtos e endereços
    """
    endereco = EnderecoSerializer()
    produto = ProdutoSerializer()

    class Meta:
        model = Saldo
        fields = ('endereco', 'produto', 'quant', )

class SaldoCustomSerializer(serializers.Serializer):
    endereco = serializers.CharField(max_length=15)
    produto  = serializers.CharField(max_length=15)
    quant    = serializers.DecimalField(max_digits=19, decimal_places=4)

    def create(self, validated_data):
        enderecos = Endereco.objects.filter(codigo=validated_data.get('endereco'))
        produtos  = Produto.objects.filter(codigo=validated_data.get('produto' ))
        if not enderecos:
            raise serializers.ValidationError('Endereço inválido %s.' % validated_data.get('endereco'))
        elif not produtos:
            raise serializers.ValidationError('Produto inválido %s.' % validated_data.get('produto'))

        endereco = enderecos[0]
        produto  = produtos[0]
        quant    = validated_data.get('quant')

        saldos = Saldo.objects.filter(endereco=endereco, produto=produto)

        if saldos:
            saldo = saldos[0]
            saldo.quant = quant
        else:
            saldo = Saldo(endereco=endereco, produto=produto, quant=quant)

        saldo.save()

        return saldo