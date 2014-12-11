# -*- coding: utf-8 -*-
from rest_framework.authentication import OAuthAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class CheckView(APIView):
    authentication_classes = (OAuthAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content={
            'user': unicode(request.user),
            'auth': unicode(request.auth),
        }
        return Response(content)