# -*- coding: ISO-8859-1 -*-
from datetime import datetime
from django.views.generic import TemplateView

from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired
from onyxlog.portaria.models.movimento import Movimento
from onyxlog.portaria.models.movimentoveiculo import MovimentoVeiculo
from onyxlog.portaria.models.movimentovisitante import MovimentoVisitante

class Index(CoreMixinLoginRequired, TemplateView):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        entradaVisitantes = MovimentoVisitante.objects.filter(
            entrada=datetime.today(),
            planta__in=request.user.perfil.plantas.all()
        ).count()
        entradaVeiculos = MovimentoVeiculo.objects.filter(
            entrada=datetime.today(),
            planta__in=request.user.perfil.plantas.all()
        ).count()
        saidas = Movimento.objects.filter(
            saida=datetime.today(),
            planta__in=request.user.perfil.plantas.all()
        ).count()
        notas = MovimentoVeiculo.objects.filter(
            nota__isnull=False, 
            entrada=datetime.today(),
            planta__in=request.user.perfil.plantas.all()
        ).order_by('-entrada','-entrada_hora',)

        portaria = {
            "entradaVisitantes" : entradaVisitantes,
            "entradaVeiculos": entradaVeiculos,
            "saidas": saidas,
            "notas": notas,
            "totalNotas": notas.count(),
        }

        context = self.get_context_data(**kwargs)
        context.update({
            "portaria": portaria,
        })
        return self.render_to_response(context)

    login_url = "/acesso/auth/"