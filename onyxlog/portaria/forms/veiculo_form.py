# -*- coding: ISO-8859-1 -*-
import datetime
from django import forms

from ..models.movimentoveiculo import MovimentoVeiculo

class MovimentoVeiculoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
        else:
            request = None

        super(MovimentoVeiculoForm, self).__init__(*args, **kwargs)

        if not request.user.is_superuser:
            self.fields['entrada'].widget.attrs['disabled'] = True
            self.fields['entrada_hora'].widget.attrs['disabled'] = True
            self.fields['saida'].widget.attrs['disabled'] = True
            self.fields['saida_hora'].widget.attrs['disabled'] = True

        if request:
            if hasattr(request.user, 'perfil'):
                self.fields['planta'].queryset = request.user.perfil.plantas.all()
        
    class Meta:
        model = MovimentoVeiculo
        fields = ['planta','entrada','entrada_hora','saida', 'saida_hora', 'motivo', 'placa', 'veiculo', 'cor', 'nota', 'fornecedor',]
        exclude = ['codigo']

class MovimentoVeiculoUpdateForm(MovimentoVeiculoForm):

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            request = kwargs.get('request')
        else:
            request = None
        super(MovimentoVeiculoUpdateForm, self).__init__(*args, **kwargs)

        if not request.user.is_superuser:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True