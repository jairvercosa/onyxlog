# -*- coding: ISO-8859-1 -*-
from django import forms
from django.forms.widgets import *
from ...cadastros.models.produto import Produto
from ...estoque.models.endereco import Endereco

class EtiquetaProdutoForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        label="Produto",
        help_text="Produto que será usado na etiqueta.",
        required=True,
    )
    
    qtd = forms.FloatField(
        label="Qtd",
        help_text="Quantidade do produto",
        required=False,
    )

    validade = forms.DateField(
        label="Validade",
        help_text="Validade do produto",
        required=False,
    )

    endereco = forms.ModelChoiceField(
        queryset=Endereco.objects.all(),
        label="Endereço",
        help_text="Endereço do produto",
        required=False,
    )

    nota = forms.CharField(
        label="Nota Fiscal",
        help_text="Nota fiscal em que o produto foi recebido",
        max_length=10,
        required=False,
    )

    pedido = forms.CharField(
        label="Pedido",
        max_length=10,
        required=False,
    )
    
    dtRecebimento = forms.DateField(
        label="Recebido em",
        help_text="Data do recebimento do produto que será impresso na etiqueta",
        required=False,
    )

    fornecedor = forms.CharField(
        label="Fornecedor do Produto",
        help_text="Nome do fornecedor que será impresso na etiqueta. \
                   Caso não seja preenchido será considerado o fornecedor preenchido \
                   no cadastro de produtos",
        max_length=120,
        required=False,
    )