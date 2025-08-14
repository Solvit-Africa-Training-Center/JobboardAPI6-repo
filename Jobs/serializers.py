from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User,
    Job,
    Application,
    Userprofile
)


class RegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=8)
    confirm_password=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        models=User
        fields= ['first_name', 'last_name','email','password', 'confirm_password','role']

    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password don't match")
        return data
        
    def create(self, validate_data):
            validate_data.pop('confirm_password')
            password= validate_data.pop('confirm_password')
            user= User(**validate_data)
            user.set_password(password)
            user.save()

        #LoginSerializers

class Login(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        email= data.get('email', None)
        password=data.get('password', None)
        if not email or not password:
            raise serializers.ValidationError(' password and email mismatch')
        user=authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("please enter valid  credential")
        if not user.is_active:
            raise serializers.ValidationError('Please verify your account to be activated ')
        refresh=RefreshToken.for_user(user)

        return {
            'email':user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    
# class ApplicationSerializer(serializers.ModelSerializer):

        
        

    