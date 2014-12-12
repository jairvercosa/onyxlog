# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from ..models.unidade import Unidade

class UnidadeForm(forms.ModelForm):
    """
    Formulário
    """
    class Meta:
        model = Unidade
        
    def get_absolute_url(self):
        return reverse('cadastros.list_unidade', kwargs={'pk': self.pk})