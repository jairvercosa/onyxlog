# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired

from ..forms.reportform import ReportForm
from ..models.movimentoveiculo import *
from ..models.movimentovisitante import *

class ReportView(CoreMixinLoginRequired, TemplateView):
    template_name = "portaria/report_form.html"
    form_class = ReportForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response(self.get_context_data(form=form))
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.template_name = "portaria/report_result.html"
            objectResult = self.get_data(request.POST, form)

            filtro_txt = []
            filtro_txt.append('Do dia ' + request.POST['data_inicio'])
            filtro_txt.append(u' até o dia ' + request.POST['data_fim'])

            if request.POST['filtro'] == "1":
                filtro = u"veículos e visitantes"
            elif request.POST['filtro'] == "2":
                filtro = u"apenas veículos"
            else:
                filtro = "apenas visitantes"
            
            filtro_txt.append(', filtrado por ' + filtro)

            if "nota" in request.POST and request.POST["nota"]:
                filtro_txt.append(', referente a nota ' + request.POST["nota"])
            
            if "placa" in request.POST and request.POST["placa"]:
                filtro_txt.append(', referente a placa ' + request.POST["placa"])

            if "cpf" in request.POST and request.POST["cpf"]:
                filtro_txt.append(', referente ao cpf ' + request.POST["cpf"])

            return self.render_to_response(self.get_context_data(object=objectResult, filtro_txt= ''.join(filtro_txt)))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_data(self, data, form):
        result = {
            "veiculos": [],
            "visitantes": [],
        }

        if data["filtro"] in ["1","2"]:
            result["veiculos"] = MovimentoVeiculo.objects.filter(
                entrada__gte= form.cleaned_data["data_inicio"],
                entrada__lte= form.cleaned_data["data_fim"],
            )

            if "nota" in data and data["nota"]:
                result["veiculos"] = result["veiculos"].filter(
                    nota = form.cleaned_data["nota"]
                )

            if "placa" in data and data["placa"]:
                result["veiculos"] = result["veiculos"].filter(
                    placa = form.cleaned_data["placa"]
                )

            if "cpf" in data and data["cpf"]:
                result["veiculos"] = result["veiculos"].filter(
                    ocupantes__cpf=form.cleaned_data["cpf"]
                )

        if data["filtro"] in ["1","3"]:
            result["visitantes"] = MovimentoVisitante.objects.filter(
                entrada__gte= form.cleaned_data["data_inicio"],
                entrada__lte= form.cleaned_data["data_fim"],
            )

            if "nota" in data and data["nota"]:
                result["visitantes"] = result["visitantes"].filter(
                    veiculo__nota= form.cleaned_data["nota"]
                )

            if "placa" in data and data["placa"]:
                result["visitantes"] = result["visitantes"].filter(
                    veiculo__placa= form.cleaned_data["placa"]
                )

            if "cpf" in data and data["cpf"]:
                result["visitantes"] = result["visitantes"].filter(
                    cpf= form.cleaned_data["cpf"]
                )

        return result