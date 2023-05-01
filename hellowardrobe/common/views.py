from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# Create your views here.


def load_initial_state(request: Request):
    pass
