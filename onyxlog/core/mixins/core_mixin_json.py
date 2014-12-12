# -*- coding: ISO-8859-1 -*-
from django import http
import json

class JSONResponseMixin(object):
    """
    Classe para resposta em json de requisicoes get
    """

    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self,context):
        return json.dumps(context)