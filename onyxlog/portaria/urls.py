from django.conf.urls import patterns, include, url

from views.index import *
from views.movimentovisitante import *
from views.movimentoveiculo import *
from views.motivo import *


urlpatterns = patterns('',
    url(r'^$', PortariaIndex.as_view(), name='portaria.portaria_index'),
    
    # movimento de visitantes
    url(r'^movimento/visitante/data/$', MovimentoVisitanteData.as_view(),name='portaria.list_json_movimentovisitante'),
    url(r'^movimento/visitante/formulario/$', MovimentoVisitanteCreateForm.as_view(),name='portaria.add_movimentovisitante'),
    url(r'^movimento/visitante/(?P<pk>\d+)/$', MovimentoVisitanteUpdateForm.as_view(),name='portaria.change_movimentovisitante'),
    url(r'^movimento/visitante/remove/(?P<pk>\d+)/$', MovimentoVisitanteDelete.as_view(),name='portaria.delete_movimentovisitante'),
    url(r'^movimento/visitante/$', MovimentoVisitanteList.as_view(), name='portaria.list_movimentovisitante'),
    url(r'^movimento/visitante/pdf/', 'onyxlog.portaria.views.movimentovisitante.pdfEtiquetaVisitante', name='portaria.etiqueta_visitante_pdf'),

    url(r'^movimento/visitante/api/fit/$', ApiVisitanteFit.as_view(),name='portaria.api_visitante_fit'),
    url(r'^movimento/visitante/api/(?P<cpf>\d+)/$', ApiVisitanteDetail.as_view(),name='portaria.api_visitante_detail'),


    # movimento de veiculos
    url(r'^movimento/veiculo/data/$', MovimentoVeiculoData.as_view(),name='portaria.list_json_movimentoveiculo'),
    url(r'^movimento/veiculo/formulario/$', MovimentoVeiculoCreateForm.as_view(),name='portaria.add_movimentoveiculo'),
    url(r'^movimento/veiculo/(?P<pk>\d+)/$', MovimentoVeiculoUpdateForm.as_view(),name='portaria.change_movimentoveiculo'),
    url(r'^movimento/veiculo/remove/(?P<pk>\d+)/$', MovimentoVeiculoDelete.as_view(),name='portaria.delete_movimentoveiculo'),
    url(r'^movimento/veiculo/$', MovimentoVeiculoList.as_view(), name='portaria.list_movimentoveiculo'),

    # motivos
    url(r'^motivo/data/$', MotivoData.as_view(),name='portaria.list_json_motivo'),
    url(r'^motivo/formulario/$', MotivoCreateForm.as_view(),name='portaria.add_motivo'),
    url(r'^motivo/(?P<pk>\d+)/$', MotivoUpdateForm.as_view(),name='portaria.change_motivo'),
    url(r'^motivo/remove/(?P<pk>\d+)/$', MotivoDelete.as_view(),name='portaria.delete_motivo'),
    url(r'^motivo/$', MotivoList.as_view(), name='portaria.list_motivo'),
)
