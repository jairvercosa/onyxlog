# -*- coding: ISO-8859-1 -*-
import datetime
from django import forms

from ..models.movimentoveiculo import MovimentoVeiculo

class MovimentoVeiculoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MovimentoVeiculoForm, self).__init__(*args, **kwargs)

        self.fields['entrada'].widget.attrs['disabled'] = True
        self.fields['entrada_hora'].widget.attrs['disabled'] = True
        self.fields['saida'].widget.attrs['disabled'] = True
        self.fields['saida_hora'].widget.attrs['disabled'] = True
        
    class Meta:
        model = MovimentoVeiculo
        fields = ['entrada','entrada_hora','saida', 'saida_hora', 'motivo', 'placa', 'veiculo', 'cor', 'nota', 'fornecedor',]
        exclude = ['codigo']

class MovimentoVeiculoUpdateForm(MovimentoVeiculoForm):

    def __init__(self, *args, **kwargs):
        super(MovimentoVeiculoUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = True