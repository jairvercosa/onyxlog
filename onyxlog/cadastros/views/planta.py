# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from ...core.base.core_base_datatable import CoreBaseDatatableView
from ...core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired

from ..models.planta import Planta

class PlantaList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'planta_list.html'
    
class PlantaData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Planta
    columns = ['nome', 'buttons', ]
    order_columns = ['nome',]
    max_display_length = 500
    url_base_form = '/cadastros/planta/'
    
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

class PlantaCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Planta
    template_name = 'planta_form.html'
    success_url = '/'

class PlantaUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Planta
    template_name = 'planta_form.html'
    success_url = '/'

class PlantaDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Planta
    success_url = '/cadastros/planta/'