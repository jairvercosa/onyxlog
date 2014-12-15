# -*- coding: ISO-8859-1 -*-
from django import forms

from ...cadastros.models.planta import Planta

class EtiquetaAutoForm(forms.Form):
    planta = forms.ModelChoiceField(queryset=Planta.objects.all(), label="Planta")
    zona_de = forms.CharField(label="Da Zona", max_length=3)
    zona_ate = forms.CharField(label="Até a Zona", max_length=3)
    instalacao_de = forms.CharField(label="Da Instalação", max_length=5)
    instalacao_ate = forms.CharField(label="Até a Instalação", max_length=5)
    rua_de = forms.CharField(label="Da Rua", max_length=3)
    rua_ate = forms.CharField(label="Até a Rua", max_length=3)
    estante_de = forms.CharField(label="Da Estante", max_length=3)
    estante_ate = forms.CharField(label="Até a Estante", max_length=3)
    prateleira_de = forms.CharField(label="Da Prateleira", max_length=3)
    prateleira_ate = forms.CharField(label="Até a Prateleira", max_length=3)