# -*- coding: ISO-8859-1 -*-
from model_mommy import mommy

from onyxlog.core.base.core_base_test import Testsbase
from onyxlog.core.models.parametro import Parametro
from onyxlog.core.models.filial import Filial

class TestsParametros(Testsbase):
    modelStandard = Parametro
    modelMommy = 'core.Parametro'
    urlBase = '/core/parametros/'
    fieldTestRender = 'nome'
    dataInsert = {
        'nome'  : 'PAR_01',
        'descricao' : 'Par teste',
        'valor' : '01',
        'filial': None
    }

    def prepare_to_post(self, fromDef):
        """
        Prepara dados para testar post
        """
        filial = mommy.make('core.Filial',responsavel=self.user)
        self.user.filiais.add(filial)
        self.user.save()
        self.dataInsert['filial'] = filial.id

        if fromDef == 'test_insert':
            self.modelPost = self.dataInsert
        else:
            self.modelRow = mommy.make(self.modelStandard, filial=filial)
            self.modelPost = self.dataInsert