# -*- coding: ISO-8859-1 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User

from ...cadastros.models import Planta

class UsuarioCreateForm(UserCreationForm):
    """
    Formulário de usuários
    """
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        exclude = ('last_login','is_staff','date_joined','is_superuser', 'password', 'groups','user_permissions', )

    def __init__(self, *args, **kwargs):
        super(UsuarioCreateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'is_active', 
            'password1', 
            'password2', 
        ]

    def get_absolute_url(self):
        return reverse('acesso.list_usuario', kwargs={'pk': self.pk})

class UsuarioUpdateForm(UserChangeForm):
    """
    Formulário de usuários
    """
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    plantas = forms.MultipleChoiceField(
        label="Plantas de Operação",
        help_text='Plantas de operação que o usuário tem acesso. Mantenha o "Control", \
        ou "Command" no Mac, pressionado para selecionar mais de uma opção.',
        required=False,
        choices=((item.id, item.nome) for item in Planta.objects.all())
    )
    m2mSave  = False
    
    class Meta:
        model = User
        exclude = ('last_login','is_staff','date_joined','is_superuser',)

    def __init__(self, *args, **kwargs):
        super(UsuarioUpdateForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'username', 'first_name', 'last_name', 'password', 'email', 
            'telefone', 'is_active', 'groups', 'plantas', 'user_permissions',
        ]

    def clean_password(self):
        """
        Permite alteração da senha no formulário de usuários
        """
        if len(self.cleaned_data.get('password')):
            return make_password(self.cleaned_data.get('password'))
        else:
            return self.initial["password"]

    def save(self, commit=True):
        instance = super(UsuarioUpdateForm,self).save(commit=False)
        old_save_m2m = self.save_m2m #guarda antiga função para campos manytomany

        def save_m2m():
            if not self.m2mSave:
                #old_save_m2m()
                instance.user_permissions.clear()
                instance.groups.clear()

                for permission in self.cleaned_data['user_permissions']:
                    instance.user_permissions.add(permission)

                for group in self.cleaned_data['groups']:
                    instance.groups.add(group)

                #self.m2mSave = True
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance