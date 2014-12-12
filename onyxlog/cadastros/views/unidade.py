# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from onyxlog.core.base.core_base_datatable import CoreBaseDatatableView
from onyxlog.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired

from ..models.unidade import Unidade
from ..forms.unidadeform import UnidadeForm

class UnidadeList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'unidade_list.html'
    
class UnidadeData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Unidade
    columns = ['nome', 'buttons', ]
    order_columns = ['nome',]
    max_display_length = 500
    url_base_form = '/cadastros/unidade/'
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class UnidadeCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Unidade
    template_name = 'unidade_form.html'
    success_url = '/'
    form_class = UnidadeForm

class UnidadeUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Unidade
    template_name = 'unidade_form.html'
    success_url = '/'
    form_class = UnidadeForm

class UnidadeDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Unidade
    success_url = '/cadastros/unidade/'