from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from django.utils.translation import gettext_lazy as _


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        super().get_header(request)
        auth_token = request.COOKIES.get('authToken', '')
        auth_token_dict = json.loads(auth_token) if auth_token else {}
        header = 'Bearer ' + \
            auth_token_dict["access"] if auth_token_dict else ''
        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)
        return header
