from django.db.models import query
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt 
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes

from clerk.serializers import ClerkSerializer, ClerkCreateSerializer, ClerkUpdateSerializer
from .models import Clerk
    
    

class ClerkViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Clerk.objects.all()

    def get_queryset(self):
        q = self.parse_valid_query_params()
        if self.action == 'list':
            if bool(q):
                queryset = Clerk.objects.filter(**q)
                return queryset
            else:
                return Clerk.objects.all()         
        else:
            return Clerk.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClerkCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ClerkUpdateSerializer
        else:
            return ClerkSerializer

        

    def destroy(self, request, pk, *args, **kwargs):
        clerk = get_object_or_404(Clerk, id=pk)
        user = clerk.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Usefull function
    def parse_valid_query_params(self):
        q = self.request.query_params
        valid_query_params = ['personal_no', 'name', 'rank', 'unit', 'subunit', 'starting_date']
        q_dict = {}
        for key in q.keys():
            if key in valid_query_params:
                q_dict[key] = q[key]

        return q_dict
                




