# -*- coding: ISO-8859-1 -*-
import json
import datetime
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from rest_framework import viewsets

from ...core.base.core_base_datatable import CoreBaseDatatableView
from ...core.mixins.core_mixin_form import CoreMixinForm, CoreMixinDel, CoreMixinPassRequestForm
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired
from ...core.mixins.core_mixin_json import JSONResponseMixin

from ...cadastros.models import Planta

from ..models.movimentovisitante import MovimentoVisitante
from ..models.movimentoveiculo import MovimentoVeiculo, MovimentoVeiculoSerializer

from ..forms.visitante_form import MovimentoVisitanteForm
from ..forms.veiculo_form import MovimentoVeiculoForm, MovimentoVeiculoUpdateForm

class MovimentoVeiculoList(CoreMixinLoginRequired, TemplateView):
    """
    View para renderização da lista
    """
    template_name = 'portaria/movimentoveiculo_list.html'
    
class MovimentoVeiculoData(CoreMixinLoginRequired, CoreBaseDatatableView):
    """
    View para renderização da lista
    """
    model = MovimentoVeiculo
    columns = [ 'planta', 'entrada', 'entrada_hora', 'saida', 'saida_hora', 'codigo', 'veiculo', 'placa', 'nota', 'fornecedor', 'buttons', ]
    order_columns = ['planta', 'entrada', 'entrada_hora', 'saida', 'codigo', 'placa', 'nota', ]
    max_display_length = 500
    url_base_form = '/portaria/movimento/veiculo/'

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
        elif column == 'planta':
            sReturn = row.planta.codigo
            return sReturn
        else:
            return super(MovimentoVeiculoData, self).render_column(row, column)

    def get_initial_queryset(self):
        qs = super(MovimentoVeiculoData, self).get_initial_queryset()
        if hasattr(self.request.user, 'perfil'):
            qs = qs.filter(planta__in=self.request.user.perfil.plantas.all())

        return qs
    
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
                    q = Q(codigo__istartswith=part)|Q(veiculo__istartswith=part) \
                       |Q(placa__istartswith=part)|Q(nota__istartswith=part) \
                       |Q(fornecedor__istartswith=part)|Q(planta__codigo__istartswith=part)

                qs_params = qs_params | q if qs_params else q

            qs = qs.filter(qs_params)

        return qs

class MovimentoVeiculoCreateForm(CoreMixinLoginRequired, CreateView, CoreMixinForm, CoreMixinPassRequestForm):
    model = MovimentoVeiculo
    template_name = 'portaria/movimentoveiculo_form.html'
    success_url = '/'
    form_class = MovimentoVeiculoForm

    def get_form_kwargs(self):
        kwargs = super(MovimentoVeiculoCreateForm, self).get_form_kwargs()
        if hasattr(self, 'object'):
            if not self.object:
                kwargs.update({
                    'initial': {
                        "entrada": datetime.date.today(),
                        "entrada_hora": datetime.datetime.now().time(),
                    }
                })
            
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None

        # pega os ocupantes do carro
        ocupantes = [json.loads(item) for item in request.POST.getlist('ocupantes[]')]

        if not ocupantes:
            return self.render_to_json_reponse(
                context={
                    'success':False, 
                    'message': 'Não foram preenchidos ocupantes para o veículo.'
                },
                status=400
            )

        for ocupante in ocupantes:
            ocupante.update({
                'motivo': request.POST.get('motivo'),
                'planta': request.POST.get('planta'),
            })
            
            ocupate_form = MovimentoVisitanteForm(ocupante, request=request)
            if not ocupate_form.is_valid():
                return self.render_to_json_reponse(
                    context={
                        'success':False, 
                        'message': 'Revise os dados dos ocupantes, alguns estão inconsistentes.'
                    },
                    status=400
                )
             
        form_class = self.get_form_class()
        form = self.get_form(form_class)   
        if form.is_valid():
            return self.form_valid(form, ocupantes)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, ocupantes):
        response = super(MovimentoVeiculoCreateForm, self).form_valid(form)
        dataToLabel = []
        
        for ocupante in ocupantes:
            visitante = MovimentoVisitante(
                cpf = ocupante['cpf'],
                nome = ocupante['nome'],
                empresa = ocupante['empresa'],
                entrada = self.object.entrada,
                entrada_hora = self.object.entrada_hora,
                veiculo = self.object,
                liberado_por = self.object.liberado_por,
                obs = self.object.obs,
                planta = Planta.objects.get(pk=ocupante['planta']),
            )

            if self.object.saida:
                visitante.saida = self.object.saida
                visitante.saida_hora = self.object.saida_hora

            visitante.save()
            dataToLabel.append(visitante.pk)

        self.request.session['dataEtiquetaVisitante'] = dataToLabel
        return self.render_to_json_reponse(
            context={
                'success':True, 
                'message': 'Registro salvo com sucesso...'
            },
            status=200
        )

class MovimentoVeiculoUpdateForm(CoreMixinLoginRequired, UpdateView, CoreMixinForm, CoreMixinPassRequestForm):
    """
    Formulário de criação
    """
    model = MovimentoVeiculo
    template_name = 'portaria/movimentoveiculo_update_form.html'
    success_url = '/'
    form_class = MovimentoVeiculoUpdateForm

    def get_form_kwargs(self):
        kwargs = super(MovimentoVeiculoUpdateForm, self).get_form_kwargs()
        if hasattr(self, 'object'):
            if self.object.entrada and not self.object.saida:
                kwargs.update({
                    'initial': {
                        "saida": datetime.date.today(),
                        "saida_hora": datetime.datetime.now().time(),
                    }
                })

        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)   
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        super(MovimentoVeiculoUpdateForm, self).form_valid(form)
        visitantes = self.object.ocupantes.all()
        visitantes.update(
            saida=self.object.saida,
            saida_hora=self.object.saida_hora)
        
        return self.render_to_json_reponse(
            context={
                'success':True, 
                'message': 'Registro salvo com sucesso...'
            },
            status=200
        )

    def form_invalid(self, form):
        return self.render_to_json_reponse(
            context={
                'success':False, 
                'message': 'Não foi possível realizar a saída do veículo'
            },
            status=400
        )

class MovimentoVeiculoDelete(CoreMixinLoginRequired, CoreMixinDel):
    """
    View de exclusão de itens
    """
    model = MovimentoVeiculo
    success_url = '/portaria/movimento/veiculo/'

class ApiVeiculoDetail(CoreMixinLoginRequired, JSONResponseMixin, TemplateView):
    """
    Retorna em json
    """
    def get(self, request, *args, **kwargs):
        veiculos = MovimentoVeiculo.objects.filter(placa=self.kwargs.get('placa', None), saida__isnull=False) \
                                              .order_by('-saida')

        if veiculos:
            veiculo = veiculos[0]
            data = {
                "placa": veiculo.placa,
                "veiculo": veiculo.veiculo,
                "cor": veiculo.cor,
            }
        else:
            data = {
                "placa": '',
                "veiculo": '',
                "cor": '',
            }

        context = data
        
        return self.render_to_response(context)
