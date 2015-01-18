# -*- coding: ISO-8859-1 -*-
import datetime
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from rest_framework import viewsets

from ...core.base.core_base_datatable import CoreBaseDatatableView
from ...core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired

from ..models.movimentovisitante import MovimentoVisitante, MovimentoVisitanteSerializer
from ..forms.visitante_form import MovimentoVisitanteForm, MovimentoVisitanteUpdateForm

class MovimentoVisitanteList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'portaria/movimentovisitante_list.html'
    
class MovimentoVisitanteData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = MovimentoVisitante
    columns = [ 'entrada', 'entrada_hora', 'saida', 'saida_hora', 'codigo', 'cpf', 'nome', 'liberado_por', 'buttons', ]
    order_columns = ['entrada', 'saida', 'codigo', 'cpf', 'nome', ]
    max_display_length = 500
    url_base_form = '/portaria/movimento/visitante/'

    def render_column(self, row, column):
        if column == 'entrada':
            sReturn = row.entrada.strftime('%d/%m/%Y')
            return sReturn
        elif column == 'saida':
            if row.saida:
                sReturn = row.saida.strftime('%d/%m/%Y')
            else:
                sReturn = ''
            return sReturn
        else:
            return super(MovimentoVisitanteData, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        """
        Filtros da query baseado no datatable
        """
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            search_parts = sSearch.split('+')
            qs_params = None
            for part in search_parts:
                try:
                    q = Q(entrada=datetime.datetime.strptime(part, '%d/%m/%Y'))|Q(saida=datetime.datetime.strptime(part, '%d/%m/%Y'))
                except:
                    q = Q(codigo__istartswith=part)|Q(cpf__istartswith=part)|Q(nome__istartswith=part)|Q(liberado_por__istartswith=part)

                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class MovimentoVisitanteCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm):
    model = MovimentoVisitante
    template_name = 'portaria/movimentovisitante_form.html'
    success_url = '/'
    form_class = MovimentoVisitanteForm

    def get_form_kwargs(self):
        kwargs = super(MovimentoVisitanteCreateForm, self).get_form_kwargs()
        if hasattr(self, 'object'):
            if not self.object:
                kwargs.update({
                    'initial': {
                        "entrada": datetime.date.today(),
                        "entrada_hora": datetime.datetime.now().time(),
                    }
                })
            
        return kwargs

class MovimentoVisitanteUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm):
    """
    Formulário de criação
    """
    model = MovimentoVisitante
    template_name = 'portaria/movimentovisitante_update_form.html'
    success_url = '/'
    form_class = MovimentoVisitanteUpdateForm

    def get_form_kwargs(self):
        kwargs = super(MovimentoVisitanteUpdateForm, self).get_form_kwargs()
        if hasattr(self, 'object'):
            if self.object.entrada:
                kwargs.update({
                    'initial': {
                        "saida": datetime.date.today(),
                        "saida_hora": datetime.datetime.now().time(),
                    }
                })

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.registerExit():
            return self.render_to_json_reponse(
                context={
                    'success':True, 
                    'message': 'Registro salvo com sucesso...'
                },
                status=200
            )
        else:
            return self.render_to_json_reponse(
                context={
                    'success':False, 
                    'message': 'Não foi possível realizar a saída do visitante...'
                },
                status=400
            )

class MovimentoVisitanteDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = MovimentoVisitante
    success_url = '/portaria/movimento/visitante/'

class ApiEntradaVisitante(viewsets.ModelViewSet):
    queryset = MovimentoVisitante.objects.all()
    serializer_class = MovimentoVisitanteSerializer