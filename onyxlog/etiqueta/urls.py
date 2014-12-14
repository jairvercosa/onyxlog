from django.conf.urls import patterns, include, url

from views.etiqueta import EtiquetaIndex, EtiquetaProduto

urlpatterns = patterns('',
    url(r'^$', EtiquetaIndex.as_view(), name='etiqueta_index'),
    
    url(r'^produto/pdf/', 'onyxlog.etiqueta.views.etiqueta.pdfEtiquetaProduto', name='etiqueta.etiqueta_produto_pdf'),
    url(r'^produto/', EtiquetaProduto.as_view(), name='etiqueta.etiqueta_produto'),

)
