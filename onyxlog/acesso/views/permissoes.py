# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.shortcuts import redirect

from onyxlog.core.base.core_base_datatable import CoreBaseDatatableView
from onyxlog.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired

class PermissoesList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de permissões
    """
    template_name = 'permissao_list.html'
    
class PermissoesData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de permissões
    """
    model = Permission
    columns = ['id','name', 'codename', 'buttons']
    order_columns = ['id','name']
    max_display_length = 500
    url_base_form = '/acesso/permissoes/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(name__istartswith=part)|Q(codename__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)
        return qs

class PermissoesCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação de permissões
    """
    model = Permission
    template_name = 'permissao_form.html'
    success_url = '/'

class PermissoesUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação de permissões
    """
    model = Permission
    template_name = 'permissao_form.html'
    success_url = '/'

class PermissoesDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Permission
    success_url = '/acesso/permissoes/'