from django.urls import path,include
from  .views import UserRegistrationView
from .views import CustomTokenObtainPairView,JobViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

urlpatterns= [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
]

#When we used Viewset we are recommended to use Defaoult router

router =DefaultRouter()
router.register(r'jobs', JobViewSet, basename='jobs')

urlpatterns= [
    path('', include(router.urls)),

]