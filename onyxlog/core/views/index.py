# -*- coding: ISO-8859-1 -*-
from django.views.generic import TemplateView

from onyxlog.core.mixins.core_mixin_login import CoreMixinLoginRequired

class Index(CoreMixinLoginRequired, TemplateView):
    template_name = "index.html"

    login_url = "/acesso/auth/"