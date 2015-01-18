# -*- coding: ISO-8859-1 -*-
from django.db import models
from rest_framework import serializers

from .movimento import Movimento
from .movimentoveiculo import MovimentoVeiculoSerializer

class MovimentoVisitante(Movimento):
    """
    Movimentos de entrada e saída de visitantes
    """

    cpf = models.CharField(
        verbose_name="CPF",
        help_text="Utilize apenas números. Não utilize caracteres como ., - ou /",
        max_length=11,
        blank=False,
        null=False,
        default=''
    )

    nome = models.CharField(
        verbose_name="Nome",
        max_length=100,
        blank=False,
        null=False
    )

    empresa = models.CharField(
        verbose_name="Empresa",
        max_length=60,
        blank=True,
        null=True
    )

    veiculo = models.ForeignKey(
        'portaria.MovimentoVeiculo',
        verbose_name="Veículo",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="ocupantes"
    )

    class Meta:
        app_label="portaria"

class MovimentoVisitanteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializador
    """

    class Meta:
        model = MovimentoVisitante
        fields = ('tipo', 'data', 'cpf', 'nome', 'empresa', 'liberado_por', )
