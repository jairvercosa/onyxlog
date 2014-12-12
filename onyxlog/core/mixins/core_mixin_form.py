# -*- coding: ISO-8859-1 -*-
import json
from django.http import HttpResponse
from django.views.generic.edit import FormView, DeleteView
from django.core.urlresolvers import resolve
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect

from onyxlog.core.mixins.core_mixin_base import CoreMixinDispatch

class CoreMixin():
    """
    Mixin para funções padrões da aplicação
    """
    def render_to_json_reponse(self, context, **response_kwargs):
        if response_kwargs['status'] == 400:
            context['message'] = 'Existem erros no formulário.'
        
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

class CoreMixinPassRequestForm(FormView):
    """
    Mixin padrão para passar request para formulário
    """
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(CoreMixinPassRequestForm, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs.update({'instance': self.object})
        return kwargs

class CoreMixinForm(FormView, CoreMixin, CoreMixinDispatch):
    """
    Mixin para funções padrões dos formulários
    """

    #Retorno para invalidez do formulário
    def form_invalid(self, form):
        return self.render_to_json_reponse(form.errors, status=400)
        
    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        response = super(FormView, self).form_valid(form)
        #self.object = form.save()
        return self.render_to_json_reponse(context={'success':True, 'message': 'Registro salvo com sucesso...'},status=200)

class CoreMixinDel(DeleteView, CoreMixin):
    """
    Mixin para funções deleções
    """
    def delete(self, request, *args, **kwargs):
        if not request.user.has_perm(resolve(request.path).url_name):
            return self.render_to_json_reponse(context={'message':'Infelizmente você não tem permissão para excluir este item.'}, status=403)
        else:
            try:
                result = super(CoreMixinDel, self).delete(self, request, *args, **kwargs)
                return self.render_to_json_reponse(context={},status=200)
            except ProtectedError:
                return self.render_to_json_reponse(context={
                    'message':'Este registro não pode ser excluido pois está sendo utilizado em outras áreas da aplicação.'
                }, status=403)
            except:
                return self.render_to_json_reponse(context={
                    'message':'Isso é frustrante mas, infelizmente um erro inesperado ocorreu. \
                                Estamos trabalhando para solucioná-lo o mais rápido possível. Desculpe! :('
                }, status=403)

    def get(self, request, *args, **kwargs):
        """
        Get da view
        """
        return redirect(self.success_url)