# -*- coding: ISO-8859-1 -*-
import datetime
from django import forms
from django_localflavor_br.forms import BRCPFField

from ..models.movimentovisitante import MovimentoVisitante

class MovimentoVisitanteForm(forms.ModelForm):
    error_messages_cnpj={
        'invalid': "CPF Inválido",
        'digits_only': "Utilize apenas números, não utilize caractereres como '.', '/' ou '-'.",
        'max_digits': "Este campo requer 11 dígitos",
    }
    cpf = BRCPFField(
        error_messages=error_messages_cnpj, 
        label="CPF", 
        help_text="Utilize apenas números. Não utilize caracteres como ., - ou /"
    )

    def __init__(self, *args, **kwargs):
        super(MovimentoVisitanteForm, self).__init__(*args, **kwargs)

        self.fields['entrada'].widget.attrs['disabled'] = True
        self.fields['entrada_hora'].widget.attrs['disabled'] = True
        self.fields['saida'].widget.attrs['disabled'] = True
        self.fields['saida_hora'].widget.attrs['disabled'] = True
        
    class Meta:
        model = MovimentoVisitante
        fields = ['entrada','entrada_hora','saida', 'saida_hora', 'motivo', 'cpf', 'nome', 'empresa', 'liberado_por', 'obs',]
        exclude = ['codigo']

class MovimentoVisitanteUpdateForm(MovimentoVisitanteForm):

    def __init__(self, *args, **kwargs):
        super(MovimentoVisitanteUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = True