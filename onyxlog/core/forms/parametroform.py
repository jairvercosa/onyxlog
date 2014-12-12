# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from onyxlog.core.models.parametro import Parametro

class ParametroForm(forms.ModelForm):
    """
    Formulário de parâmetros
    """
    class Meta:
        model = Parametro
        
    def get_absolute_url(self):
        return reverse('core.list_parametro', kwargs={'pk': self.pk})