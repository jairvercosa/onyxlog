# -*- coding: ISO-8859-1 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from onyxlog.core.base.core_base_test import Testsbase
from django.contrib.auth.models import Group

class TestsGroup(Testsbase):
    modelStandard = Group
    modelMommy = 'auth.Group'
    urlBase = '/acesso/grupos/'
    fieldTestRender = 'name'
    dataInsert = {
        'name'  : 'PAR_01',
    }

    def addPermissions(self):
        """
        Adiciona permissoes ao usuario
        """
        #busca tabela de models
        if not self.modelStandard is None:
            contentItem = ContentType.objects.get(app_label='auth',model='group')
            #busca permissoes do model
            if not contentItem:
                self.assertTrue(False)

            permissions = Permission.objects.all().filter(content_type=contentItem.id)
        
            for permission in permissions:
                self.user.user_permissions.add(permission)