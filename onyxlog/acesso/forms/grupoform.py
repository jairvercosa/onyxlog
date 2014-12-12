# -*- coding: ISO-8859-1 -*-
from django import forms
from django.contrib.auth.models import Group

class GrupoCreateForm(forms.ModelForm):
    """
    Formulário de Grupos
    """
    
    class Meta:
        model = Group
        exclude = ('permissions',)

    def get_absolute_url(self):
        return reverse('acesso.list_group', kwargs={'pk': self.pk})