# -*- coding: ISO-8859-1 -*-
from django.test import TestCase

class TestsIndex(TestCase):

    #Testa redirecionamento quando não logado
    def test_index_redirect_no_login(self):
        # Faz chamada da pagina principal
        response = self.client.get('/')
        self.assertRedirects(response, 'acesso/auth/?next=/', status_code=302, target_status_code=200, msg_prefix='')