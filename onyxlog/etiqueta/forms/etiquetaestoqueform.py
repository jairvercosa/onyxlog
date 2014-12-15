# -*- coding: ISO-8859-1 -*-
from django import forms
from django.forms.widgets import *
from ...estoque.models.endereco import Endereco

class EtiquetaEnderecoForm(forms.Form):
    codigo_de = forms.ModelChoiceField(
        queryset=Endereco.objects.all(),
        label="Do Endereço",
        required=True,
    )
    
    codigo_ate = forms.ModelChoiceField(
        queryset=Endereco.objects.all(),
        label="Até o Endereço",
        required=True,
    )

    def get_absolute_url(self):
        return reverse('etiqueta.etiqueta_endereco')