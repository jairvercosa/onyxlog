# -*- coding: ISO-8859-1 -*-
from django.test import TestCase

from onyxlog.acesso.models.usuario import Usuario

class TestLogin(TestCase):
    """
    Testes da aplicação para login
    """
    
    #Testes de Renderização
    def test_render_login_form(self):
        # Faz chamada da pagina principal
        response = self.client.get('/acesso/auth/')
        
        # Verifica se renderiza campo csrf
        self.assertContains(response, "<input type='hidden' name='csrfmiddlewaretoken'", status_code=200)

        # Verifica se renderiza campo username
        self.assertContains(response, '<input class="form-control" id="id_username" name="username"', status_code=200)

        # Verifica se renderiza campo senha
        self.assertContains(response, '<input class="form-control" id="id_senha" name="senha"', status_code=200)

    #Testa falhas login inválido
    def test_login_invalid_data_form(self):
        #Faz chamada da pagina principal com dados
        response = self.client.post('/acesso/auth/', {
            'username': '',
            'senha'   : '',
        })

        self.assertFormError(response, 'form', 'username', u'Este campo \xe9 obrigat\xf3rio')
        self.assertFormError(response, 'form', 'senha', u'Este campo \xe9 obrigat\xf3rio')

    #Testa falhas login inválido
    def test_login_invalid_user_or_pass_form(self):
        #Faz chamada da pagina principal com dados
        response = self.client.post('/acesso/auth/', {
            'username': 'teste',
            'senha'   : 'teste',
        })

        self.assertEqual(response.status_code, 400)

    #Testa se login foi realizado
    def test_login_form_successfull(self):
        data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com'
        }
        user = Usuario.objects.create_user(data['username'], data['email'], data['senha'])

        #Faz chamada da pagina principal com dados
        response = self.client.post('/acesso/auth/', data)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='')
    
    #Testa se faz logout
    def test_login_form_successfull(self):
        data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com'
        }
        user = Usuario.objects.create_user(data['username'], data['email'], data['senha'])

        #Faz chamada da pagina principal com dados
        response = self.client.post('/acesso/auth/', data)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='')

        # Faz chamada do logou
        response = self.client.get('/acesso/sair/')
        self.assertRedirects(response, 'acesso/auth/', status_code=302, target_status_code=200, msg_prefix='')
