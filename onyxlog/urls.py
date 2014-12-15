from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('onyxlog.core.urls'),name="App-Principal"),

    url(r'^core/', include('onyxlog.core.urls')),
    url(r'^acesso/', include('onyxlog.acesso.urls')),
    url(r'^cadastros/', include('onyxlog.cadastros.urls')),
    url(r'^etiquetas/', include('onyxlog.etiqueta.urls')),
    url(r'^estoque/', include('onyxlog.estoque.urls')),
    # Examples:
    # url(r'^$', 'onyxlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

handler403 = 'onyxlog.core.views.core.error403'
handler404 = 'onyxlog.core.views.core.error404'
handler500 = 'onyxlog.core.views.core.error500'