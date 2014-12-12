# -*- coding: ISO-8859-1 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from onyxlog.core.base.core_base_test import Testsbase
from django.contrib.auth.models import Permission

class TestsPermission(Testsbase):
    modelStandard = Permission
    modelMommy = 'auth.Permission'
    urlBase = '/acesso/permissoes/'
    fieldTestRender = 'name'
    dataInsert = {
        'name'  : 'Pode Peqs1',
        'content_type'  : 2,
        'codename' : 'can1',
    }

    def addPermissions(self):
        """
        Adiciona permissoes ao usuario
        """
        #busca tabela de models
        if not self.modelStandard is None:
            contentItem = ContentType.objects.get(app_label='auth',model='permission')
            #busca permissoes do model
            if not contentItem:
                self.assertTrue(False)

            permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
            for permission in permissions:
                self.user.user_permissions.add(permission)