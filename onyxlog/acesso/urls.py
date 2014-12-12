from django.conf.urls import patterns, include, url

from onyxlog.acesso.views.login import Login, sair
from onyxlog.acesso.views.usuarios import UsuariosList, UsuariosData, UsuariosCreateForm, UsuariosUpdateForm, UsuariosDelete, UsuariosSetPassForm
from onyxlog.acesso.views.grupos import GruposList, GruposData, GruposCreateForm, GruposUpdateForm, GruposDelete
from onyxlog.acesso.views.permissoes import PermissoesList, PermissoesData, PermissoesCreateForm, PermissoesUpdateForm, PermissoesDelete

urlpatterns = patterns('',
    url(r'^auth/', Login.as_view()),

    #Usuarios
    url(r'^usuarios/data/$', UsuariosData.as_view(),name='acesso.list_json_usuario'),
    url(r'^usuarios/formulario/$', UsuariosCreateForm.as_view(),name='acesso.add_usuario'),
    url(r'^usuarios/(?P<pk>\d+)/$', UsuariosUpdateForm.as_view(),name='acesso.change_usuario'),
    url(r'^usuarios/password/$', UsuariosSetPassForm.as_view(),name='acesso.change_pass_usuario'),
    url(r'^usuarios/remove/(?P<pk>\d+)/$', UsuariosDelete.as_view(),name='acesso.delete_usuario'),
    url(r'^usuarios/$', UsuariosList.as_view(), name='acesso.list_usuario'),

    #Grupos
    url(r'^grupos/data/$', GruposData.as_view(),name='auth.list_json_group'),
    url(r'^grupos/formulario/$', GruposCreateForm.as_view(),name='auth.add_group'),
    url(r'^grupos/(?P<pk>\d+)/$', GruposUpdateForm.as_view(),name='auth.change_group'),
    url(r'^grupos/remove/(?P<pk>\d+)/$', GruposDelete.as_view(),name='auth.delete_group'),
    url(r'^grupos/$', GruposList.as_view(), name='auth.list_group'),

    #Permissoes
    url(r'^permissoes/data/$', PermissoesData.as_view(),name='auth.list_json_permission'),
    url(r'^permissoes/formulario/$', PermissoesCreateForm.as_view(),name='auth.add_permission'),
    url(r'^permissoes/(?P<pk>\d+)/$', PermissoesUpdateForm.as_view(),name='auth.change_permission'),
    url(r'^permissoes/remove/(?P<pk>\d+)/$', PermissoesDelete.as_view(),name='auth.delete_permission'),
    url(r'^permissoes/$', PermissoesList.as_view(), name='auth.list_permission'),
    
    url(r'^sair/', sair, name='sair'),
)