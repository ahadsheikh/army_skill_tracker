from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt 
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes

from clerk.serializers import ClerkSerializer, ClerkCreateSerializer, ImageUploadSerializer, ClerkRetrievekSerializer
from .models import Clerk
    
    

class ClerkViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Clerk.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClerkCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ClerkRetrievekSerializer
        else:
            return ClerkSerializer

    def destroy(self, request, pk, *args, **kwargs):
        clerk = get_object_or_404(Clerk, id=pk)
        user = clerk.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(('GET',))
def user_type(requst, id):
    user = get_object_or_404(User, id=id)
    if user.is_superuser:
        return Response({'related_id': 0, 'type': 'admin'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'clerk'):
        return Response({'related_id': user.clerk.id, 'type': 'clerk'}, status=status.HTTP_200_OK)
    elif hasattr(user, 'officer'):
        return Response({'related_id': 0, 'type': 'officer'}, status=status.HTTP_200_OK)
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
        else:
            return Response({"message": "User not have a clerk"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_201_CREATED)


class IsAdmin(generics.GenericAPIView):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)

        res = {}
        res['is_admin'] = user.is_superuser

        return Response(res, status=status.HTTP_200_OK)
