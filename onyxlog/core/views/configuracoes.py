# -*- coding: ISO-8859-1 -*-
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin

from onyxlog.core.mixins.core_mixin_base import CoreMixinDispatch

class Configuracoes(LoginRequiredMixin, TemplateView, CoreMixinDispatch):
    template_name = "configuracoes.html"
    login_url = "/acesso/auth/"