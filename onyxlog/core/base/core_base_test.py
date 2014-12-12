# -*- coding: ISO-8859-1 -*-
"""
Teste base para ser herdado por todos os testes padrões
"""
from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from onyxlog.acesso.models.usuario import Usuario
from model_mommy import mommy

class Testsbase(TestCase):
    modelStandard = None
    urlBase = None
    fieldTestRender = None
    dataInsert = None
    modelPost = None
    modelRow = None
    modelMommy = None
    
    def setUp(self):
        self.data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com'
        }
        self.user = Usuario.objects.create_user(self.data['username'], self.data['email'], self.data['senha'])
        self.client.login(username=self.data['username'], password=self.data['senha'])

    def test_permissions(self):
        """
        Testa se valida permissoes de acesso
        """
        if not self.urlBase is None:
            #Teste de insert
            response = self.client.get(self.urlBase+'formulario/')
            self.assertEquals(response.status_code, 403)

            #Cria dados
            self.prepare_to_post('test_permissions')

            #Teste de update
            response = self.client.post(self.urlBase+str(self.modelRow.id)+'/', self.modelPost)
            self.assertEquals(response.status_code, 403)

            #Teste de delete
            response = self.client.post(self.urlBase+'remove/'+str(self.modelRow.id)+'/',{})
            self.assertEquals(response.status_code, 403)

    def addPermissions(self):
        """
        Adiciona permissoes ao usuario
        """
        #busca tabela de models
        if not self.modelStandard is None:
            model = self.modelStandard()
            contentItem = ContentType.objects.get(app_label=model._meta.app_label,model=model.__class__.__name__.lower())
            #busca permissoes do model
            if not contentItem:
                self.assertTrue(False)

            permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
            for permission in permissions:
                self.user.user_permissions.add(permission)

    def test_render_listpage(self):
        """
        Testa renderização da página de lista
        """
        # Faz chamada da pagina
        if not self.urlBase is None:
            response = self.client.get(self.urlBase)
            self.assertEquals(response.status_code, 200)

    def test_return_data_to_list(self):
        """
        Testa retorno de dados em json
        """
        # Faz chamada da pagina
        if not self.urlBase is None:
            response = self.client.get(self.urlBase+'data/')
            self.assertContains(response, '"result": "ok"', status_code=200)

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelMommy)
            self.modelPost = self.dataInsert

    def test_insert(self):
        """
        Testa renderização do formulário para iniclusão
        """
        self.addPermissions()
        # Faz chamada da pagina
        if not self.urlBase is None:
            response = self.client.get(self.urlBase+'formulario/')
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'name="'+self.fieldTestRender+'"', status_code=200)

        """
        Testa gravação dos dados no post de inclusão
        """
        
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.prepare_to_post('test_insert')
            response = self.client.post(self.urlBase+'formulario/', self.modelPost)
            self.assertContains(response, '"success": true', status_code=200)

    def test_update(self):
        """
        Testa post do formulário de edição
        """
        
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.addPermissions()
            self.prepare_to_post('test_update')
            response = self.client.post(self.urlBase+str(self.modelRow.id)+'/', self.modelPost)
            self.assertContains(response, '"success": true', status_code=200)

    def test_delete(self):
        """
        Testa delete
        """
        # Faz chamada da pagina
        if not self.urlBase is None:
            self.addPermissions()
            self.prepare_to_post('test_delete')

            if not self.modelRow:
                self.assertTrue(False)

            totalBefore = self.modelStandard.objects.count()
            response = self.client.post(self.urlBase+'remove/'+str(self.modelRow.id)+'/',{})
            totalUpdated = self.modelStandard.objects.count()
        
            self.assertEquals(response.status_code, 200)
            self.assertTrue(totalBefore > totalUpdated)