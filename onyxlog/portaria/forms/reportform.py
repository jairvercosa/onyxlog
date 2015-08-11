# -*- coding: utf-8 -*-

from django import forms

class ReportForm(forms.Form):
    data_inicio = forms.DateField(label="Do dia")
    data_fim = forms.DateField(label=u"Até o dia")

    CHOICE_FILTER = (
        ('1',u'Veículos e Visitantes'),
        ('2',u'Apenas Veículos'),
        ('3',u'Apenas Visitantes'),
    )
    filtro = forms.ChoiceField(choices=CHOICE_FILTER)
    nota = forms.CharField(max_length=30, required=False)
    placa = forms.CharField(max_length=30, required=False)
    cpf = forms.CharField(max_length=20, required=False)
    