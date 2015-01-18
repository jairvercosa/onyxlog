from django.conf.urls import patterns, include, url
from rest_framework import routers

from views.index import *
from views.movimentovisitante import *
from views.movimentoveiculo import *

router = routers.DefaultRouter()
router.register(r'visitante',ApiEntradaVisitante)

urlpatterns = patterns('',
    url(r'^$', PortariaIndex.as_view(), name='portaria.portaria_index'),
    
    # movimento de visitantes
    url(r'^movimento/visitante/data/$', MovimentoVisitanteData.as_view(),name='portaria.list_json_movimentovisitante'),
    url(r'^movimento/visitante/formulario/$', MovimentoVisitanteCreateForm.as_view(),name='portaria.add_movimentovisitante'),
    url(r'^movimento/visitante/(?P<pk>\d+)/$', MovimentoVisitanteUpdateForm.as_view(),name='portaria.change_movimentovisitante'),
    url(r'^movimento/visitante/remove/(?P<pk>\d+)/$', MovimentoVisitanteDelete.as_view(),name='portaria.delete_movimentovisitante'),
    url(r'^movimento/visitante/$', MovimentoVisitanteList.as_view(), name='portaria.list_movimentovisitante'),

    # api
    url(r'^movimento/api/', include(router.urls)),

    # movimento de veiculos
    url(r'^movimento/veiculo/data/$', MovimentoVeiculoData.as_view(),name='portaria.list_json_movimentoveiculo'),
    url(r'^movimento/veiculo/formulario/$', MovimentoVeiculoCreateForm.as_view(),name='portaria.add_movimentoveiculo'),
    url(r'^movimento/veiculo/(?P<pk>\d+)/$', MovimentoVeiculoUpdateForm.as_view(),name='portaria.change_movimentoveiculo'),
    url(r'^movimento/veiculo/remove/(?P<pk>\d+)/$', MovimentoVeiculoDelete.as_view(),name='portaria.delete_movimentoveiculo'),
    url(r'^movimento/veiculo/$', MovimentoVeiculoList.as_view(), name='portaria.list_movimentoveiculo'),
)
