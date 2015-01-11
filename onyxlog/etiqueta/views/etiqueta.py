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

from ..forms.etiquetaestoqueform import EtiquetaEnderecoForm
from ..forms.etiquetaprodutoform import EtiquetaProdutoForm
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
                "produto"       : item['id'],
                "qtd"           : item['qtd'],
                "endereco"      : item['endereco'],
                "validade"      : item['validade'],
                "nota"          : item['nota'],
                "pedido"        : item['pedido'],
                "dtRecebimento" : item['dtRecebimento'],
                "fornecedor"    : item['fornecedor'],
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
            if posted['endereco']:
                endereco = Endereco.objects.get(pk=posted['endereco']).codigo
            else:
                endereco = ''

            if produto.validade and not posted['validade']:
                return self.render_to_json_reponse(context={
                        'success':False, 
                        'message': 'Existem produtos que controlam validade e que a mesma não foi preenchida.'
                    },status=400)

            data.append({
                "codigo": produto.codigo,
                "descricao": produto.desc,
                "qtd": posted['qtd'],
                "endereco": endereco,
                "validade": posted['validade'],
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
        logo_company = settings.STATIC_ROOT+'/img/logo_company_label.jpg'
        logo_company2 = settings.STATIC_ROOT+'/img/logo_company_label2.jpg'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiquetas_produto.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=(378,264))
    
    for produto in data:
        # cabeçalho
        p.drawImage(logo_company,5,228,)
        p.drawImage(logo_company2,292,228,)
        p.drawString(122, 239, "Etiqueta de Identificação.")

        # label dos detalhes
        p.setFontSize(7)
        p.rect(5,191,365,31,fill=0)
        p.drawString(7,214, "Produto")

        p.rect(5,160,80,31,fill=0)
        p.drawString(7,183, "UN")

        p.rect(85,160,90,31,fill=0)
        p.drawString(88,183, "Qtd")

        p.rect(175,160,90,31,fill=0)
        p.drawString(178,183, "Nota")

        p.rect(265,160,105,31,fill=0)
        p.drawString(268,183, "Pedido")

        p.rect(5,129,365,31,fill=0)
        p.drawString(7,152, "Fornecedor")

        p.rect(265,129,105,31,fill=0)
        p.drawString(268,152, "Validade")

        # box do codigo de barras
        p.rect(5,10,220,119,fill=0)
        
        p.rect(225,72,145,57,fill=0)
        p.drawString(227,121, "Código do Produto")
        p.rect(225,75,145,40,fill=1)

        p.rect(225,41,145,31,fill=0)
        p.drawString(227,65, "Endereço")

        p.rect(225,10,145,31,fill=0)
        p.drawString(227,34, "Recebimento")


        # imprime os dados
        p.setFontSize(10)
        p.drawString(7,200, produto['descricao'])

        p.setFontSize(16)
        p.drawString(17 ,167, produto['un'])
        p.drawString(88 ,167, produto['qtd'])
        p.drawString(178,167, produto['nota'])
        p.drawString(268,167, produto['pedido'])
        p.drawString(17 ,136, produto['fornecedor'])
        p.drawString(268,136, produto['validade'])
        p.drawString(242,19 , produto['recebimento'])

        # codigo de barras
        barcode = code128.Code128(produto['codigo'],barWidth=0.5*mm,barHeight=30*mm)
        barcode.drawOn(p,5,35)
        p.setFontSize(10)
        p.drawCentredString(120,15, produto['codigo'])

        p.setFontSize(16)
        p.setFillColorRGB(255,255,255)
        p.drawString(230,90, produto['codigo'])

        p.setFontSize(14)
        p.setFillColorRGB(0,0,0)
        p.drawString(230,50, produto['endereco'])
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
        logo_company = settings.STATIC_ROOT+'/img/logo_company_label.jpg'
        logo_company2 = settings.STATIC_ROOT+'/img/logo_company_label2.jpg'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etiqueta_endereco.pdf"'

    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=(378,264))

    for endereco in data:
        # cabeçalho
        p.drawImage(logo_company,5,228,)
        p.drawImage(logo_company2,292,228,)
        p.drawCentredString(193, 249, "Etiqueta de Identificação.")
        p.drawCentredString(193, 231, "de Endereço.")

        # label dos detalhes
        p.setFontSize(7)
        p.rect(5,191,365,31,fill=0)
        p.drawString(12,214, "Planta")

        p.rect(5,129,365,62,fill=0)
        p.drawString(12,183, "Endereço")

        # box do codigo de barras
        p.rect(5,10,365,119,fill=0)
        
        # imprime os dados
        p.setFontSize(16)
        p.drawString(17,198, endereco['planta'])

        p.setFontSize(22)
        p.drawCentredString(188,151, endereco['codigo'])
        
        # codigo de barras
        barcode = code128.Code128(endereco['codigo'],barWidth=0.5*mm,barHeight=30*mm)
        barcode.drawOn(p,50,35)
        p.showPage()

    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

