from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError

from clerk.serializers import ImageUploadSerializer
from core.serializers import SoldierSerializer
from core.models import Soldier

    

@api_view(('GET',))
def user_type(requst, id):
    user = get_object_or_404(User, id=id)
    if user.is_superuser:
        return Response({'related_id': -1, 'type': 'admin'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'clerk'):
        return Response({'related_id': user.clerk.id, 'type': 'clerk'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'officer'):
        return Response({'related_id': user.officer.id, 'type': 'officer'}, status=status.HTTP_200_OK)
    else:
        return Response({'related_id': 0, 'type': 'unknown'}, status=status.HTTP_200_OK)



class ProfilePicUpload(generics.GenericAPIView):
    serializer_class = ImageUploadSerializer
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['image']
        user = get_object_or_404(User, pk=id)

        if hasattr(user, 'clerk'):
            clerk = user.clerk
            clerk.image = file
            clerk.profile_pic.save(file.name, file, save=True)
            return Response(status=status.HTTP_200_OK)
        elif hasattr(user, 'officer'):
            officer = user.officer
            officer.image = file
            officer.profile_pic.save(file.name, file, save=True)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response({"message": "User not a clerk nor a officer"}, status=status.HTTP_404_NOT_FOUND)



class IsAdmin(generics.GenericAPIView):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)

        res = {}
        res['is_admin'] = user.is_superuser

        return Response(res, status=status.HTTP_200_OK)

class SolvierViewset(viewsets.ModelViewSet):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer

    def get_queryset(self):
        q = self.parse_valid_query_params()
        if self.action == 'list':
            if bool(q):
                try:
                    queryset = Soldier.objects.filter(**q)
                except ValidationError as v:
                    queryset = Soldier.objects.none()
                return queryset
            else:
                return Soldier.objects.all()         
        else:
            return Soldier.objects.all()

    def parse_valid_query_params(self):
        q = self.request.query_params
        valid_query_params = ['personal_no', 'name', 'rank', 'address', 'unit',
                        'subunit', 'appointment', 'join_date', 'commision_date', 
                        'previous_company', 'mission']
        q_dict = {}
        for key in q.keys():
            if key in valid_query_params:
                q_dict[key] = q[key]

        return q_dict