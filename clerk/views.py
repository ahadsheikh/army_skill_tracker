from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import jwt 

from clerk.serializers import ClerkSerializer, ClerkCreateSerializer
from .models import Clerk


class ClerkCreateView(generics.GenericAPIView):

    def post(self, request):
        serializer = ClerkCreateSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['name'],
                last_name=serializer.validated_data['name']
            )

            clerk = Clerk.objects.create(
                username=serializer.validated_data['username'],
                name=serializer.validated_data['name'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                type="C",
                rank=serializer.validated_data['rank'],
                address=serializer.validated_data['address'],
                unit=serializer.validated_data['unit'],
                subunit=serializer.validated_data['subunit'], 
                contact=serializer.validated_data['contact'],
            )
            serializer = ClerkSerializer(clerk)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ClerkViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    serializer_class = ClerkSerializer
    queryset = Clerk.objects.all()

# class ClerkPicUpload(generics.GenericAPIView):
#     def post(self, request):


class DecodeJWT(generics.GenericAPIView):
    def post(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            decoded = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(id=decoded['user_id'])
            clerk = Clerk.objects.get(username=user.username)
            decoded['clerk_id'] = clerk.id
            res = {}
            res['user_id'] = decoded['user_id']
            res['clerk_id'] = decoded['clerk_id']
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
