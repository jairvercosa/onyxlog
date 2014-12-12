# -*- coding: ISO-8859-1 -*-
from braces.views import LoginRequiredMixin

class CoreMixinLoginRequired(LoginRequiredMixin):
    login_url = "/acesso/auth/"