# -*- coding: ISO-8859-1 -*-
from django.db import models
from rest_framework import serializers

from .movimento import Movimento

class MovimentoVeiculo(Movimento):
    """
    Movimentos de entrada e saída de veículos
    """

    placa = models.CharField(
        verbose_name="Placa",
        max_length=7,
        blank=False,
        null=False,
    )

    veiculo = models.CharField(
        verbose_name="Veículo",
        help_text="Ex. Fiat Pálio, Gol, Caminhão Scannia.",
        max_length=60,
        blank=False,
        null=False,
    )


    cor = models.CharField(
        verbose_name="Cor",
        help_text="Descreva a cor do veículo.",
        max_length=30,
        blank=False,
        null=False,
    )

    nota = models.CharField(
        verbose_name="Nota Fiscal",
        help_text="Nota fiscal que está sendo entregue.",
        max_length=20,
        blank=True,
        null=True
    )

    fornecedor = models.CharField(
        verbose_name="Fornecedor",
        max_length=80,
        blank=True,
        null=True
    )

    class Meta:
        app_label="portaria"

class MovimentoVeiculoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """

    class Meta:
        model = MovimentoVeiculo
        fields = ('tipo', 'data', 'veiculo', 'placa', 'cor', 'liberado_por', )
        