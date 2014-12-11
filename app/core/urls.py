from django.conf.urls import patterns, url
from app.core.views.core import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='core_index'),
)