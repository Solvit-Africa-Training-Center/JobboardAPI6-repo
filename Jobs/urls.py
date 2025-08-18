from django.urls import path, include
from .views import UserRegistrationView, CustomTokenObtainPairView, JobViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

# Router for ViewSet
router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='jobs')

# Combine router and manual paths
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]