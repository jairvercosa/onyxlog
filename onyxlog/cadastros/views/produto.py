# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import Http404

from onyxlog.core.base.core_base_datatable import CoreBaseDatatableView
from onyxlog.core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired
from onyxlog.core.mixins.core_mixin_json import JSONResponseMixin

from ..models.produto import Produto

class ProdutoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'produto_list.html'
    
class ProdutoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = Produto
    columns = ['codigo', 'desc', 'revisao', 'grupo', 'buttons', ]
    order_columns = ['codigo', 'desc', 'revisao']
    max_display_length = 500
    url_base_form = '/cadastros/produto/'
    
    def render_column(self, row, column):
        if column == 'grupo':
            sReturn = row.grupo.nome
            return sReturn
        else:
            return super(ProdutoData, self).render_column(row, column)

    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(codigo__istartswith=part)|Q(desc__istartswith=part)|Q(revisao__istartswith=part)|Q(grupo__nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs
    
class ProdutoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Produto
    template_name = 'produto_form.html'
    success_url = '/'

class ProdutoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = Produto
    template_name = 'produto_form.html'
    success_url = '/'

class ProdutoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = Produto
    success_url = '/cadastros/produto/'

class ApiProdutoFit(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json os produtos
    """
    def get(self, request, *args, **kwargs):
        sSearch = self.request.GET.get('term', None)

        data = []
        qs = []
        if sSearch:
            qs = Produto.objects.all()
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                q = Q(codigo__istartswith=part)|Q(desc__istartswith=part)|Q(revisao__istartswith=part)|Q(grupo__nome__istartswith=part)
                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        for item in qs:
            data.append({
                "id": item.pk,
                "desc": item.codigo + ' - ' + item.desc,
            })

        context = data
        
        return self.render_to_response(context)

class ApiProdutoDetail(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json os produtos
    """
    def get(self, request, *args, **kwargs):
        produto = Produto.objects.get(pk=self.kwargs.get('pk', None))

        data = {
            "id": produto.pk,
            "codigo": produto.codigo,
            "desc": produto.desc,
            "unidade": produto.unidade.nome,
            "fornecedor": produto.fornecedor,
            "validade": produto.validade,
        }
        
        context = data
        
        return self.render_to_response(context)