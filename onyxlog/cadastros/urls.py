from django.conf.urls import patterns, include, url

from views.index import Index
from views.unidade import *
from views.produto import *
from views.grupo import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='cadastros_index'),

    # unidade
    url(r'^unidade/data/$', UnidadeData.as_view(),name='cadastros.list_json_unidade'),
    url(r'^unidade/formulario/$', UnidadeCreateForm.as_view(),name='cadastros.add_unidade'),
    url(r'^unidade/(?P<pk>\d+)/$', UnidadeUpdateForm.as_view(),name='cadastros.change_unidade'),
    url(r'^unidade/remove/(?P<pk>\d+)/$', UnidadeDelete.as_view(),name='cadastros.delete_unidade'),
    url(r'^unidade/$', UnidadeList.as_view(), name='cadastros.list_unidade'),

    # produto
    url(r'^produto/data/$', ProdutoData.as_view(),name='cadastros.list_json_produto'),
    url(r'^produto/formulario/$', ProdutoCreateForm.as_view(),name='cadastros.add_produto'),
    url(r'^produto/(?P<pk>\d+)/$', ProdutoUpdateForm.as_view(),name='cadastros.change_produto'),
    url(r'^produto/remove/(?P<pk>\d+)/$', ProdutoDelete.as_view(),name='cadastros.delete_produto'),
    url(r'^produto/$', ProdutoList.as_view(), name='cadastros.list_produto'),

    # grupo de produtos
    url(r'^grupo-produto/data/$', GrupoProdutoData.as_view(),name='cadastros.list_json_grupoproduto'),
    url(r'^grupo-produto/formulario/$', GrupoProdutoCreateForm.as_view(),name='cadastros.add_grupoproduto'),
    url(r'^grupo-produto/(?P<pk>\d+)/$', GrupoProdutoUpdateForm.as_view(),name='cadastros.change_grupoproduto'),
    url(r'^grupo-produto/remove/(?P<pk>\d+)/$', GrupoProdutoDelete.as_view(),name='cadastros.delete_grupoproduto'),
    url(r'^grupo-produto/$', GrupoProdutoList.as_view(), name='cadastros.list_grupoproduto'),
)
