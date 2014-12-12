# -*- coding: ISO-8859-1 -*-
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve

class CoreMixinDispatch(View):
    """
    Controla as permissões do sistema
    """
    def dispatch(self, request, *args, **kwargs):
        urlName = resolve(request.path).url_name
        if "_min" in urlName:
            urlName = urlName[:-4]
            
        if not request.user.has_perm(urlName):
            raise PermissionDenied()
        return super(CoreMixinDispatch, self).dispatch(request, *args, **kwargs)