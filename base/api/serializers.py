from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import UserProfile



class UserRegisterSerializer(serializers.ModelSerializer):
   
    print('inside serializer')
    password = serializers.CharField(write_only=True) 
    password2 = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')  

    def validate(self, data):
        print('inside confirm password')
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ('username', 'password', 'first_name', 'last_name', 'email')  
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']