# -*- coding: utf-8 -*-
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from app.core.mixins import CoreLoginRequired

class IndexView(TemplateView, CoreLoginRequired):
    template_name = 'core/index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)