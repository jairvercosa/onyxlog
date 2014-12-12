# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from ..models.grupo import GrupoProduto

class GrupoProdutoForm(forms.ModelForm):
    """
    Formulário
    """
    class Meta:
        model = GrupoProduto
        
    def get_absolute_url(self):
        return reverse('cadastros.list_grupoproduto', kwargs={'pk': self.pk})