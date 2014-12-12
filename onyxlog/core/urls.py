from django.conf.urls import patterns, include, url

from views.index import Index
from views.configuracoes import Configuracoes

from views.parametros import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='core_index'),
    url(r'^configuracoes/', Configuracoes.as_view(), name='core.core_configurations'),

    #Parametros
    url(r'^parametros/data/$', ParametrosData.as_view(),name='core.list_json_parametro'),
    url(r'^parametros/formulario/$', ParametrosCreateForm.as_view(),name='core.add_parametro'),
    url(r'^parametros/(?P<pk>\d+)/$', ParametrosUpdateForm.as_view(),name='core.change_parametro'),
    url(r'^parametros/remove/(?P<pk>\d+)/$', ParametrosDelete.as_view(),name='core.delete_parametro'),
    url(r'^parametros/$', ParametrosList.as_view(), name='core.list_parametros'),
)
