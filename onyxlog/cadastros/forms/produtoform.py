# -*- coding: ISO-8859-1 -*-
import re
from datetime import date
from django import forms

from ..models.produto import Produto

class ProdutoForm(forms.ModelForm):
    """
    Formulário
    """
    class Meta:
        model = Produto
        
    def get_absolute_url(self):
        return reverse('cadastros.list_produto', kwargs={'pk': self.pk})