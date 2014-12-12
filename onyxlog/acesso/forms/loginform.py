# -*- coding: ISO-8859-1 -*-
from django import forms

class LoginForm(forms.Form):
    """
    Formulário de Login da aplicação
    """
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Usuário',
            }
        ), 
        error_messages={
            'required': 'Este campo é obrigatório',
        }
    )
    senha = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Senha',
            }
        ), 
        error_messages={
            'required': 'Este campo é obrigatório',
        }
    )