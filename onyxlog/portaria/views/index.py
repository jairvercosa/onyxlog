# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import TemplateView
from ...core.mixins.core_mixin_login import CoreMixinLoginRequired

class PortariaIndex(CoreMixinLoginRequired, TemplateView):
    template_name = "portaria/portaria_menu.html"