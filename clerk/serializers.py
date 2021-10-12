from rest_framework import serializers
from .models import Clerk
from django.contrib.auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
            'username': {'validators': []},
        }


class ClerkCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Clerk
        fields = ('user', 'personal_no', 'name', 'password', 'rank', 'address', 
                            'unit', 'subunit', 'contact')

    def create(self, validated_data):
        userData = validated_data.pop('user', None)
        user = User.objects.create(
            username=userData['username'],
            email=userData['email'],
        )
        user.set_password(userData['password'])
        user.save()
        validated_data['user'] = user

        # Ending the clerk duty period
        Clerk.objects.latest('starting_date').end_officer_duty()

        return Clerk.objects.create(**validated_data)
    

class ClerkUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Clerk
        fields = ('user', 'personal_no', 'name', 'password', 'rank', 'address', 
                        'unit', 'subunit', 'contact')

    def update(self, instance, validated_data):
        print("adsf")
        user = instance.user
        userdata = validated_data.pop('user', None)
        user.username = userdata.get('username', user.username)
        user.email = userdata.get('email', user.email)
        user.save()

        instance.user = user
        instance.name = validated_data.get('name', instance.name)
        instance.personal_no = validated_data.get('personal_no', instance.personal_no)
        instance.password = validated_data.get('password', instance.password)
        instance.rank = validated_data.get('rank', instance.rank)
        instance.address = validated_data.get('address', instance.address)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.subunit = validated_data.get('subunit', instance.subunit)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.save()
        return instance


class ClerkSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Clerk
        fields = ('user', 'id', 'personal_no', 'name', 'password', 
                        'rank', 'address', 'unit', 'subunit', 'starting_date', 
                        'ending_date', 'contact', 'profile_pic')

                        
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()