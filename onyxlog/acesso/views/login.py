# -*- coding: ISO-8859-1 -*-
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from onyxlog.acesso.forms.loginform import LoginForm

class Login(FormView):
    """
    View de login para validar autenticação de Usuário
    """
    
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            nextUrl = '/'
            if 'next' in request.GET.keys():
                nextUrl = request.GET['next']

            return self.render_to_response(self.get_context_data(form=form,urlRedirect=nextUrl))

    #Renderiza em json a resposta
    def render_to_json_reponse(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    #Retorno para invalidez do formulário
    def form_invalid(self, form):
        response = super(Login, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_reponse(form.errors, status=400)
        else:
            return response
        
    #Retorno caso o formulário seja válido
    def form_valid(self, form):
        response = super(Login, self).form_valid(form)

        userAuth = authenticate(username=self.request.POST['username'], password=self.request.POST['senha'])
        if not userAuth is None:
            if userAuth.is_active: #Usuário ativo
                login(self.request,userAuth)
                if self.request.is_ajax():
                    return self.render_to_json_reponse({'urlRedirect':'/'},status=200)
                else:
                    return redirect('/')
            else:
                return self.render_to_json_reponse({'username':['Usuário desativado']},status=400)
        elif self.request.is_ajax():
            return self.render_to_json_reponse({'csrfmiddlewaretoken':'Usuário ou senha inválido'},status=400)
        else:
            return HttpResponse(u'Usuário ou senha inválido',status=400)

def sair(request):
    """
    View para saída do sistema
    """
    logout(request)
    return redirect('/acesso/auth/')