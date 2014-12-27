# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from rest_framework import viewsets

from ...core.base.core_base_datatable import CoreBaseDatatableView
from ...core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired

from ..models.saldo import Saldo, SaldoSerializer, SaldoCustomSerializer

class SaldoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'saldo_list.html'
    
class SaldoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Saldo
    columns = ['endereco', 'produto', 'descricao', 'quant', 'buttons', ]
    order_columns = ['endereco', 'produto', ]
    max_display_length = 500
    url_base_form = '/estoque/saldo/'

    def render_column(self, row, column):
        if column == 'endereco':
            sReturn = row.endereco.codigo
            return sReturn
        elif column == 'produto':
            sReturn = row.produto.codigo
            return sReturn
        elif column == 'descricao':
            sReturn = row.produto.desc
            return sReturn
        else:
            return super(SaldoData, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(endereco__codigo__istartswith=part)|Q(produto__codigo__istartswith=part)|Q(produto__desc__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class SaldoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Saldo
    template_name = 'saldo_form.html'
    success_url = '/'

class SaldoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Saldo
    template_name = 'saldo_form.html'
    success_url = '/'

class SaldoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Saldo
    success_url = '/estoque/saldos/'

class SaldoViewSet(viewsets.ModelViewSet):
    queryset = Saldo.objects.all()
    serializer_class = SaldoCustomSerializer