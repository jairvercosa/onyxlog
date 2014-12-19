from django.conf.urls import patterns, include, url

from views.index import *
from views.endereco import *
from views.saldo import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='estoque.estoque_index'),
    
    # endereco
    url(r'^endereco/data/$', EnderecoData.as_view(),name='estoque.list_json_endereco'),
    url(r'^endereco/formulario/$', EnderecoCreateForm.as_view(),name='estoque.add_endereco'),
    url(r'^endereco/(?P<pk>\d+)/$', EnderecoUpdateForm.as_view(),name='estoque.change_endereco'),
    url(r'^endereco/remove/(?P<pk>\d+)/$', EnderecoDelete.as_view(),name='estoque.delete_endereco'),
    url(r'^endereco/$', EnderecoList.as_view(), name='estoque.list_endereco'),

    # endereco
    url(r'^saldo/data/$', SaldoData.as_view(),name='estoque.list_json_saldo'),
    url(r'^saldo/formulario/$', SaldoCreateForm.as_view(),name='estoque.add_saldo'),
    url(r'^saldo/(?P<pk>\d+)/$', SaldoUpdateForm.as_view(),name='estoque.change_saldo'),
    url(r'^saldo/remove/(?P<pk>\d+)/$', SaldoDelete.as_view(),name='estoque.delete_saldo'),
    url(r'^saldo/$', SaldoList.as_view(), name='estoque.list_saldo'),

    url(r'^endereco/automatico/$', EnderecoAuto.as_view(), name='estoque.endereco_auto'),
    
)