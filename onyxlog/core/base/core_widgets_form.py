# -*- coding: ISO-8859-1 -*-
"""
Widgets customizados para uso em formulários
"""

from django import forms
from django.utils.safestring import mark_safe

class CustomWidgetComboAdd(forms.widgets.Select):
    """
    Combo com botão de adicionar
    """
    def render(self, name, value, attrs=None):
        return mark_safe(
            '''%s<button class="btn btn-sm btn-info btn-add-combo"><i class="glyphicon glyphicon-plus"></i> Novo</button>''' \
                % (super(CustomWidgetComboAdd,self).render(name, value, attrs))
        )