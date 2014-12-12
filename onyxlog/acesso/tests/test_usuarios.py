# -*- coding: ISO-8859-1 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from onyxlog.core.base.core_base_test import Testsbase
from onyxlog.acesso.models.usuario import Usuario

class TestsUsuarios(Testsbase):
    modelStandard = Usuario
    modelMommy = 'acesso.Usuario'
    urlBase = '/acesso/usuarios/'
    fieldTestRender = 'username'
    dataInsert = {
        'username'  : 'testuserPost',
        'first_name' : 'Test',
        'last_name' : 'User',
        'email' : 'testuserpost@test.com',
        'telefone' : '(21) 99999-9999',
        'password1' : 'testpass',
        'password2' : 'testpass',
        'is_active': 1,
    }

    def addPermissions(self):
        """
        Adiciona permissoes ao usuario
        """
        #busca tabela de models
        if not self.modelStandard is None:
            contentItem = ContentType.objects.get(app_label='acesso',model='usuario')
            #busca permissoes do model
            if not contentItem:
                self.assertTrue(False)

            permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
            for permission in permissions:
                self.user.user_permissions.add(permission)

    def test_usuarios_render_form_change_pas(self):
        """
        Testa renderização do formulário de troca de senha
        """
        contentItem = ContentType.objects.get(app_label='acesso',model='usuario')
        permission = Permission(name='Can Change Pass',content_type=contentItem,codename='change_pass_usuario')
        permission.save()

        permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
        for permission in permissions:
            self.user.user_permissions.add(permission)

        # Faz chamada da pagina
        response = self.client.get('/acesso/usuarios/password/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'name="new_password1"', status_code=200)

        """
        Testa renderização do formulário de troca de senha
        """
        dataPost = {
            'new_password1'  : 'testpass2',
            'new_password2'  : 'testpass2',
        }

        response = self.client.post('/acesso/usuarios/password/', dataPost)
        self.assertEquals(response.status_code, 200)