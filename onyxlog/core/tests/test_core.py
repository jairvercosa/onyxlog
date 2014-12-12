# -*- coding: ISO-8859-1 -*-
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from onyxlog.acesso.models.usuario import Usuario

class TestsCore(TestCase):

    def setUp(self):
        self.data = {
            'username' : 'testuser',
            'senha'       : 'testpass',
            'email'       : 'test@test.com'
        }
        self.user = Usuario.objects.create_user(self.data['username'], self.data['email'], self.data['senha'])
        self.client.login(username=self.data['username'], password=self.data['senha'])
        

    #Testa render configurações
    def test_render_configuracoes(self):
        # Faz chamada da pagina
        contentItem = ContentType.objects.get(app_label='core',model='parametro')
        permission = Permission(name='Can Access Configurations',content_type=contentItem,codename='core_configurations')
        permission.save()

        permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
        for permission in permissions:
            self.user.user_permissions.add(permission)        

        response = self.client.get('/core/configuracoes/')
        self.assertEquals(response.status_code, 200)