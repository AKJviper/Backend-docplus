from .models import AppUser , UserDoctor
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class onlyGET(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return False
        