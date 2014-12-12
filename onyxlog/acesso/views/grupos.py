# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.models import Group
from django.shortcuts import redirect

from onyxlog.core.base.core_base_datatable import CoreBaseDatatableView
from onyxlog.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired

from onyxlog.acesso.forms.grupoform import GrupoCreateForm

class GruposList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de grupos
    """
    template_name = 'grupo_list.html'
    
class GruposData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de grupos
    """
    model = Group
    columns = ['id','name', 'buttons']
    order_columns = ['id','name']
    max_display_length = 500
    url_base_form = '/acesso/grupos/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(name__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)
        return qs

class GruposCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação de grupos
    """
    model = Group
    template_name = 'grupo_form.html'
    success_url = '/'
    form_class = GrupoCreateForm

class GruposUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação de grupos
    """
    model = Group
    template_name = 'grupo_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        permissions = request.POST.getlist('permissions[]')

        if form.is_valid():
            form.cleaned_data['permissions'] = permissions
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        permissions = form.cleaned_data['permissions']
        self.object = form.save()
        self.object.permissions.clear()

        for permission in permissions:
            self.object.permissions.add(permission)
        
        self.object.save()        
        return self.render_to_json_reponse({'success': True, 'message': 'Registro incluido com sucesso.'},status=200)

class GruposDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Group
    success_url = '/acesso/grupos/'