# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy
from onyxlog.core.base.core_base_test import Testsbase
from onyxlog.core.models.filial import Filial

class TestsFilial(Testsbase):
    modelStandard = Filial
    modelMommy = 'core.Filial'
    urlBase = '/core/filiais/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'matriz' : False,
        'responsavel': None,
    }

    
    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        self.dataInsert['responsavel'] = self.user.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelMommy, responsavel=self.user)
            self.modelPost = self.dataInsert