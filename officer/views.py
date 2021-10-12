from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt 
from django.shortcuts import get_object_or_404

from officer.serializers import OfficerSerializer, OfficerCreateSerializer, OfficerRetrieveSerializer
from .models import Officer
    
    

class OfficerViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Officer.objects.all()

    def get_queryset(self):
        q = self.parse_valid_query_params()
        if self.action == 'list':
            if bool(q):
                queryset = Officer.objects.filter(**q)
                return queryset
            else:
                return Officer.objects.all()         
        else:
            return Officer.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OfficerCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return OfficerRetrieveSerializer
        else:
            return OfficerSerializer

    def destroy(self, request, pk, *args, **kwargs):
        officer = get_object_or_404(Officer, id=pk)
        user = officer.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def parse_valid_query_params(self):
        q = self.request.query_params
        valid_query_params = ['ba_no', 'name', 'rank', 'unit', 'subunit', 'appointment', 'starting_date', 'ending_date']
        q_dict = {}
        for key in q.keys():
            if key in valid_query_params:
                q_dict[key] = q[key]

        return q_dict