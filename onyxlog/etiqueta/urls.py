from django.conf.urls import patterns, include, url

from views.etiqueta import EtiquetaIndex, EtiquetaProduto, EtiquetaEndereco

urlpatterns = patterns('',
    url(r'^$', EtiquetaIndex.as_view(), name='etiqueta.etiqueta_index'),
    
    url(r'^produto/pdf/', 'onyxlog.etiqueta.views.etiqueta.pdfEtiquetaProduto', name='etiqueta.etiqueta_produto_pdf'),
    url(r'^produto/', EtiquetaProduto.as_view(), name='etiqueta.etiqueta_produto'),

    url(r'^endereco/pdf/', 'onyxlog.etiqueta.views.etiqueta.pdfEtiquetaEndereco', name='etiqueta.etiqueta_endereco_pdf'),
    url(r'^endereco/', EtiquetaEndereco.as_view(), name='etiqueta.etiqueta_endereco'),
    
)
