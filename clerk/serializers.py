from rest_framework import serializers
from .models import Clerk



class ClerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clerk
        fields = ('username', 'name', 'password', 'email', 'type', 'rank', 'address', 'unit', 'subunit', 'contact')



class ClerkCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    rank = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=100)
    unit = serializers.CharField(max_length=30)
    subunit = serializers.CharField(max_length=30)
    contact = serializers.CharField(max_length=50)


# class UserCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Clerk
#         fields = ('username', 'email', 'password', 'first_name', 'last_name')


# class ClerkCreateSerializer(serializers.ModelSerializer):
#     user = UserCreateSerializer()

#     class Meta:
#         model = Clerk
#         fields = ('user', 'type', 'rank', 'address', 'unit', 'subunit', 'contact')