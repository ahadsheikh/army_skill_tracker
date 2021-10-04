from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt 
from django.shortcuts import get_object_or_404

from clerk.serializers import ClerkSerializer, ClerkCreateSerializer
from .models import Clerk
    
    

class ClerkViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Clerk.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClerkCreateSerializer
        else:
            return ClerkSerializer


# class ClerkPicUpload(generics.GenericAPIView):
#     def post(self, request):


class IsAdmin(generics.GenericAPIView):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)

        res = {}
        res['is_admin'] = user.is_superuser

        return Response(res, status=status.HTTP_200_OK)
