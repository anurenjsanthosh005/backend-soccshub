from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserSignupView, MyTokenObtainPairView, UserViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
]
