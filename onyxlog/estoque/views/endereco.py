# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from ...core.base.core_base_datatable import CoreBaseDatatableView
from ...core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired
from ...core.mixins.core_mixin_json import JSONResponseMixin

from ..models.endereco import Endereco

class EnderecoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'endereco_list.html'
    
class EnderecoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Endereco
    columns = ['planta', 'codigo', 'buttons', ]
    order_columns = ['codigo',]
    max_display_length = 500
    url_base_form = '/estoque/endereco/'

    def render_column(self, row, column):
        if column == 'planta':
            sReturn = row.planta.codigo + ' - ' + row.planta.nome
            return sReturn
        else:
            return super(EnderecoData, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(codigo__istartswith=part)|Q(planta__codigo__istartswith=part)|Q(planta__nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class EnderecoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Endereco
    template_name = 'endereco_form.html'
    success_url = '/'

class EnderecoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Endereco
    template_name = 'endereco_form.html'
    success_url = '/'

class EnderecoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Endereco
    success_url = '/estoque/endereco/'

class EnderecoAuto(CoreMixinLoginRequired, TemplateView):
    """
    View para geração automática
    """
    template_name = 'endereco_auto.html'

class ApiEnderecoFit(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json os enderecos
    """
    def get(self, request, *args, **kwargs):
        qs = Endereco.objects.all()
        data = []
        
        for item in qs:
            data.append({
                "id": item.pk,
                "codigo": item.codigo,
            })

        context = data
        
        return self.render_to_response(context)