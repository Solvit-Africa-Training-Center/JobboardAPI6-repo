from django.shortcuts import render
from rest_framework import viewsets,filters
from .models import JOb,Application,User
from .serializers import JobSerializer
from Jobs import IsCandidate, IsAdminOrRecruiter, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, LoginSerializer,ApplicationSerializer
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class UserRegistrationView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#Rolebased views based   on their permissions on systems for all recruiter  candidate and admin 
class JobViewSet(viewsets.ModelViewSet):
    queryset=JOb.objects.all()
    serializer_class= JobSerializer

    def get_permissions(self):
        '''
        Assign permission Based on action
         -list, retrieve: Any authenticated use
         -create: recruiter or admin
         -update, partial_uodate, destroy: OwnerorAdmin
        '''
        if self.action in ['list','retrieve']:
            permission_class= [IsAuthenticated]
        elif self.action == 'create':
            permission_class= {IsAuthenticated,IsAdminOrRecruiter}
        elif self.action in ['Update', 'partial_update', 'destroy']:
            permission_class = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_class = [IsAuthenticated]
        return [permission() for permission in permission_class]
    def get_serializer_context(self):
        context= super().get_serializer_context()
        context.update({"request": self.context})
        return context
    def perform_create(self, serializer):
        #This automaticall Assign the recruiter(JobOwner to) as the logged in user
        serializer.save(recruiter=self.request.user)
        
    
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset=Application
    serializer_class=ApplicationSerializer
    permission_classes= [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        user=self.request.user()
        if user.role== 'CANDIDATE':
            return self.queryset.filter(candidate=user)
        if user.role== ['RECRUITER','ADMIN']:
            return self.queryset.filter(job_recruiter=user)
        return Application.objects.none
    def get_serializer_context(self):
        # Pass request to serializer for role validation and user assignment
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

#Applications stuffs

class ApplicationPagination(PageNumberPagination):
    page_size= 10
    page_query_param= 'page_size'
    max_page_size= 50


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset=Application.objects.all()
    serializer_class=ApplicationSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user

        if user.role == User.Role.ADMIN:
            return Application.objects.all()
        elif user.role== User.Role.RECRUITER:
            return Application.objects.filter(posted_by=user)
        elif user.role== User.Role.CANDIDATE:
            return Application.objects.filter(candidate=user)
        return Application.objects.none()
    def create(self, request, *args, **kwargs):
        user= request.user

        if user.role != User.Role.CANDIDATE:
            return Response ({'details': "only candidates can apply for jobs"}, status=status.HTTP_403_FORBIDDEN)
        job_id= request.data.get(job_id)
        if not job_id:
            return Response({"detail": "JOB ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        #logic for checking if job is still exist in order to avoid double applying

        try:
            job=JOb.objects.get(id=job_id)
        except JOb.DoesNotExist:
            return Response({"detail": "JOB NOT Found."}, status=status.HTTP_404_NOT_FOUND)
        if Application.objects.filter(job=job, candidate=user).exists():
            return Response({"detail": "You have already applied for this job."}, status=status.HTTP_400_BAD_REQUEST)
        #Create Application

        application= Application.objects.create(
            job=job,
            candidate=user,
            cover_letter=request.user.data.get("cover_letter", "")
        )
        serializer= self.get-serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        application= self.get_objects()
        user=request.user

         # Only recruiters (job owner) or admins can update status
        if user.role not in [User.Role.ADMIN, User.Role.RECRUITER]:
            return Response({"detail": "Not allowed to update application status."}, status=status.HTTP_403_FORBIDDEN)

        # Recruiter can only update their job's applications
        if user.role == User.Role.RECRUITER and application.job.posted_by != user:
            return Response({"detail": "You can only update applications for your own jobs."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

