from django.conf.urls import patterns, url
from api.auth import CheckView

urlpatterns = patterns('',

    # api
    url(r'^api/check/$', CheckView.as_view(), name='autho_autho'),
)
