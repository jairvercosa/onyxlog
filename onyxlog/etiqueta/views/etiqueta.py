# -*- coding: ISO-8859-1 -*-
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings
from django.shortcuts import redirect

from ...core.mixins.core_mixin_login import CoreMixinLoginRequired
from ...core.mixins.core_mixin_base import CoreMixinDispatch
from ...core.mixins.core_mixin_form import CoreMixin, CoreMixinForm

from ..forms.etiquetaestoqueform import EtiquetaProdutoForm, EtiquetaEnderecoForm
from ...cadastros.models.produto import Produto
from ...estoque.models.endereco import Endereco

class EtiquetaIndex(CoreMixinLoginRequired, TemplateView):
    template_name = "etiqueta_menu.html"

class EtiquetaProduto(CoreMixinLoginRequired, TemplateView, CoreMixin):
    template_name = "etiqueta_list_produto.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
        
    def post(self, request, *args, **kwargs):
        dataPost = eval(request.POST.getlist('data')[0])
        dataToLabel = []

        # valida os dados digitados com o formulário
        for item in dataPost:
            dataForm = {
                "produto": item['id'],
                "nota": item['nota'],
                "pedido": item['pedido'],
                "dtRecebimento": item['dtRecebimento'],
                "fornecedor": item['fornecedor'],
            }
            form = EtiquetaProdutoForm(dataForm)

            if not form.is_valid():
                return self.render_to_json_reponse(form.errors, status=400)
            else:
                dataToLabel.append(dataForm)
        
        # prepara dados para etiqueta
        data = []
        for posted in dataToLabel:
            produto = Produto.objects.get(pk=posted['produto'])
            data.append({
                "codigo": produto.codigo,
                "descricao": produto.desc,
                "nota": posted['nota'],
                "pedido": posted['pedido'],
                "un": produto.unidade.nome,
                "grupo": produto.grupo.nome,
                "recebimento": posted['dtRecebimento'],
                "fornecedor": posted['fornecedor'],
            })

    
        if data:
            request.session['dataEtiqueta'] = data
            return self.render_to_json_reponse(context={
                'success':True, 
                'message': 'Etiquetas geradas com sucesso.',
            },status=200)
        else:
            return self.render_to_json_reponse(context={
                'success':False, 
                'message': 'Nenhum produto foi encontrado.'
            },status=400)

def pdfEtiquetaProduto(request):
    """
    Gera arquivo PDF das etiquetas solicitadas
    """

    if 'dataEtiqueta' not in request.session:
        redirect('etiqueta.etiqueta_produto')
    
    data = request.session['dataEtiqueta']
    if not data:
        redirect('etiqueta.etiqueta_produto')
        
    request.session.pop('dataEtiqueta')

    if settings.DEBUG:
        logo_company = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label.jpg'
        logo_company2 = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label2.jpg'
    else:
        logo_company = settings.BASE_DIR+'/static/img/logo_company_label.jpg'
        logo_company2 = settings.BASE_DIR+'/static/img/logo_company_label2.jpg'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas_produto.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=(386,283))
    
    for produto in data:
        # cabeçalho
        p.drawImage(logo_company,10,242,)
        p.drawImage(logo_company2,292,242,)
        p.drawString(122, 255, "Etiqueta de Identificação.")

        # label dos detalhes
        p.setFontSize(7)
        p.rect(10,205,365,31,fill=0)
        p.drawString(12,228, "Produto")

        p.rect(10,174,100,31,fill=0)
        p.drawString(12,197, "UN")

        p.rect(110,174,120,31,fill=0)
        p.drawString(112,197, "Nota")

        p.rect(230,174,145,31,fill=0)
        p.drawString(232,197, "Pedido")

        p.rect(10,143,365,31,fill=0)
        p.drawString(12,166, "Fornecedor")

        # box do codigo de barras
        p.rect(10,10,220,133,fill=0)
        
        p.rect(230,41,145,102,fill=0)
        p.drawString(232,135, "Código do Produto")

        p.rect(230,60,145,60,fill=1)

        p.rect(230,10,145,31,fill=0)
        p.drawString(232,34, "Recebimento")


        # imprime os dados
        p.setFontSize(10)
        p.drawString(12,212, produto['descricao'])

        p.setFontSize(16)
        p.drawString(22,181, produto['un'])
        p.drawString(122,181, produto['nota'])
        p.drawString(242,181, produto['pedido'])
        p.drawString(22,150, produto['fornecedor'])
        p.drawString(242,19, produto['recebimento'])

        # codigo de barras
        barcode = code128.Code128(produto['codigo'],barWidth=0.5*mm,barHeight=30*mm)
        barcode.drawOn(p,5,40)
        p.setFontSize(10)
        p.drawCentredString(120,20, produto['codigo'])

        p.setFontSize(16)
        p.setFillColorRGB(255,255,255)
        p.drawString(236,85, produto['codigo'])
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

class EtiquetaEndereco(CoreMixinLoginRequired, TemplateView, CoreMixinForm):
    template_name = "etiqueta_endereco.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] =  EtiquetaEnderecoForm()
        return self.render_to_response(context)
        
    def post(self, request, *args, **kwargs):
        form = EtiquetaEnderecoForm(request.POST)

        if not form.is_valid():
            return self.form_invalid(form)
        else:
            dataEnderecos = []
            print form.data
            enderecos = Endereco.objects.filter(
                codigo__gte=Endereco.objects.get(pk=form.data['codigo_de']).codigo,
                codigo__lte=Endereco.objects.get(pk=form.data['codigo_ate']).codigo,
            )
            
            for item in enderecos:
                dataEnderecos.append({
                    "codigo": item.codigo,
                    "planta": item.planta.nome,
                })

            request.session['dataEtiquetaEndereco'] = dataEnderecos
            return self.form_valid(form)

    def form_valid(self, form):
        response = super(EtiquetaEndereco, self).form_valid(form)
        return self.render_to_json_reponse(context={'success':True, 'message': 'Etiquetas geradas com sucesso.'},status=200)
         

def pdfEtiquetaEndereco(request):
    """
    Gera arquivo PDF das etiquetas solicitadas
    """

    if 'dataEtiquetaEndereco' not in request.session:
        redirect('etiqueta.etiqueta_endereco')
    
    data = request.session['dataEtiquetaEndereco']
    if not data:
        redirect('etiqueta.etiqueta_endereco')
    
    request.session.pop('dataEtiquetaEndereco')


    if settings.DEBUG:
        logo_company = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label.jpg'
        logo_company2 = settings.BASE_DIR+'/onyxlog/core/static/img/logo_company_label2.jpg'
    else:
        logo_company = settings.BASE_DIR+'/static/img/logo_company_label.jpg'
        logo_company2 = settings.BASE_DIR+'/static/img/logo_company_label2.jpg'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiqueta_endereco.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=(386,283))

    for endereco in data:
        # cabeçalho
        p.drawImage(logo_company,10,242,)
        p.drawImage(logo_company2,292,242,)
        p.drawCentredString(193, 263, "Etiqueta de Identificação.")
        p.drawCentredString(193, 245, "de Endereço.")

        # label dos detalhes
        p.setFontSize(7)
        p.rect(10,205,365,31,fill=0)
        p.drawString(12,228, "Planta")

        p.rect(10,143,365,62,fill=0)
        p.drawString(12,197, "Endereço")

        # box do codigo de barras
        p.rect(10,10,365,133,fill=0)
        
        # imprime os dados
        p.setFontSize(16)
        p.drawString(22,212, endereco['planta'])

        p.setFontSize(22)
        p.drawCentredString(193,165, endereco['codigo'])
        
        # codigo de barras
        barcode = code128.Code128(endereco['codigo'],barWidth=0.5*mm,barHeight=30*mm)
        barcode.drawOn(p,55,35)
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

