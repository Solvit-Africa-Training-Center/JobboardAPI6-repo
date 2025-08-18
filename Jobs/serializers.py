from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User,
    Job,
    Application,
    Userprofile,
    SavedJob,
)

#Registration serializers
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'role']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
        
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError('Both email and password are required')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError('Please verify your account before logging in')

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['user', 'resume', 'bio']


class JobSerializer(serializers.ModelSerializer):
    recruiter = UserSerializer(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'requirements',
            'company_name', 'location', 'salary',
            'category', 'job_type', 'deadline',
            'created_at', 'recruiter'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != User.Role.RECRUITER:
            raise serializers.ValidationError("Only recruiters can post jobs.")
        validated_data['recruiter'] = user
        return super().create(validated_data)


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='job', write_only=True
    )
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'candidate', 'job_id', 'job',
            'cover_letter', 'cv', 'status', 'applied_at'
        ]
        read_only_fields = ['id', 'candidate', 'job', 'status', 'applied_at']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != User.Role.CANDIDATE:
            raise serializers.ValidationError("Only candidates can apply to jobs.")
        validated_data['candidate'] = user
        return super().create(validated_data)

class SavedJobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show user email
    job = JobSerializer(read_only=True)  # nested job details
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='job', write_only=True
    )

    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'job_id', 'saved_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        # prevent duplicate save
        job = validated_data['job']
        if SavedJob.objects.filter(user=user, job=job).exists():
            raise serializers.ValidationError("You have already saved this job.")

        return super().create(validated_data)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims (optional)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra fields to the response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
        }

        return data