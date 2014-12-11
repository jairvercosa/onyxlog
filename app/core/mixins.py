# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin

class CoreLoginRequired(LoginRequiredMixin):
    login_url = '/autho/login/'
