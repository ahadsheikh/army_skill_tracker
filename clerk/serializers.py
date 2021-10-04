from rest_framework import serializers
from .models import Clerk
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ClerkCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Clerk
        fields = ('user', 'name', 'password', 'rank', 'address', 'unit', 'subunit', 'contact')

    def create(self, validated_data):
        user = validated_data.pop('user', None)
        user = User.objects.create(**user)
        return Clerk.objects.create(**validated_data)


class ClerkSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Clerk
        fields = ('user', 'name', 'password', 'rank', 'address', 'unit', 'subunit', 'contact')
    
    def update(self, instance, validated_data):
        user = instance.user
        userdata = validated_data.pop('user', None)
        user.username = userdata.get('username', user.username)
        user.email = userdata.get('username', user.email)
        user.first_name = userdata.get('first_name', user.first_name)
        user.last_name = userdata.get('first_name', user.last_name)
        user.save()

        instance.user = user
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.address = validated_data.get('address', instance.address)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.subunit = validated_data.get('subunit', instance.subunit)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.save()
        return instance