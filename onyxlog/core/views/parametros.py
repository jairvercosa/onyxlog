# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from onyxlog.core.base.core_base_datatable import CoreBaseDatatableView
from onyxlog.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired
from onyxlog.core.models.parametro import Parametro
from onyxlog.core.forms.parametroform import ParametroForm

class ParametrosList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista de parâmetros
    """
    template_name = 'parametro_list.html'
    
class ParametrosData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista de parâmetros
    """
    model = Parametro
    columns = ['nome', 'descricao', 'buttons']
    order_columns = ['nome','descricao']
    max_display_length = 500
    url_base_form = '/core/parametros/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__istartswith=part)|Q(descricao__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class ParametrosCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação de parâmetros
    """
    model = Parametro
    template_name = 'parametro_form.html'
    success_url = '/'
    form_class = ParametroForm

class ParametrosUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação de parâmetros
    """
    model = Parametro
    template_name = 'parametro_form.html'
    success_url = '/'
    form_class = ParametroForm

class ParametrosDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Parametro
    success_url = '/core/parametros/'