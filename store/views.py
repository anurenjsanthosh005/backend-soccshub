from rest_framework import viewsets, permissions,generics
from .models import Product
from .serializers import ProductCreateSerializer, ProductSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer, MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone (even guest users) can view products
            return [permissions.AllowAny()]
        # Only admin can create, update, delete products
        return [permissions.IsAdminUser()]
        
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        length = self.request.query_params.get('length')
        category = self.request.query_params.get('category')

        if length:
            queryset = queryset.filter(length=length)
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        return queryset
    
# Signup view
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can sign up

# Login view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        except Exception:
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserViewSet(viewsets.ModelViewSet):
    """
    Read-only API to list users. Only admin can see this.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
