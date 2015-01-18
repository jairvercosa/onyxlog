# -*- coding: ISO-8859-1 -*-
import os
import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
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

    def form_valid(self, form):
        response = super(MovimentoVisitanteCreateForm, self).form_valid(form)
        self.request.session['dataEtiquetaVisitante'] = [self.object.pk]
        
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...'},status=200)

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

def pdfEtiquetaVisitante(request):
    """
    Gera arquivo PDF das etiquetas solicitadas
    """

    if 'dataEtiquetaVisitante' not in request.session:
        redirect('portaria.movimentovisitante_list')
    
    data = request.session.pop('dataEtiquetaVisitante')
    if not data:
        redirect('portaria.movimentovisitante_list')
        
    if settings.DEBUG:
        logo_company = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label.jpg'
        logo_company2 = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label2.jpg'
    else:
        logo_company = settings.STATIC_ROOT+'/img/logo_company_label.jpg'
        logo_company2 = settings.STATIC_ROOT+'/img/logo_company_label2.jpg'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="visitantes_etiqueta.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=(378,264))
    visitantes = MovimentoVisitante.objects.filter(pk__in=data)

    for visitante in visitantes:
        # cabeçalho
        p.drawImage(logo_company,5,228,)
        p.drawImage(logo_company2,292,228,)
        p.drawString(122, 239, "Identificação de Visitantes")

        # label dos detalhes
        p.setFontSize(7)
        p.rect(5,191,365,31,fill=0)
        p.drawString(7,214, "Nome")

        p.rect(5,160,120,31,fill=0)
        p.drawString(7,183, "Documento")

        p.rect(125,160,120,31,fill=0)
        p.drawString(128,183, "Veículo")

        p.rect(245,160,125,31,fill=0)
        p.drawString(253,183, "Entrada")

        p.rect(5,129,365,31,fill=0)
        p.drawString(7,152, "Empresa")

        # box do codigo de barras
        p.rect(5,10,365,119,fill=0)
        
        # imprime os dados
        p.setFontSize(16)
        p.drawString(10,200, visitante.nome)

        p.setFontSize(16)
        p.drawString(10 ,167, visitante.cpf)
        if visitante.veiculo:
            p.drawString(131 ,167, visitante.veiculo.placa)

        p.setFontSize(10)
        p.drawString(256,167, visitante.entrada.strftime('%d/%m/%Y') + ' ' + visitante.entrada_hora.strftime('%I:%M'))

        p.setFontSize(16)
        p.drawString(10,137, visitante.empresa)
        
        # codigo de barras
        p.setFontSize(10)
        p.drawCentredString(188,15, visitante.codigo)
        
        # codigo de barras
        barcode = code128.Code128(visitante.codigo,barWidth=0.5*mm,barHeight=30*mm)
        barcode.drawOn(p,95,35)
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response