from rest_framework import serializers
from .models import Product, ProductImage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    existing_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'discount',
            'is_active', 'length_type', 'category', 'images', 'existing_images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image in images_data:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        existing_image_ids = validated_data.pop('existing_images', [])

        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete images not in existing_images (both DB + media files)
        images_to_delete = ProductImage.objects.filter(product=instance).exclude(id__in=existing_image_ids)
        for img in images_to_delete:
            if img.image and img.image.storage.exists(img.image.name):
                img.image.delete(save=False)
        images_to_delete.delete()

        # Add new uploaded images
        for image in images_data:
            ProductImage.objects.create(product=instance, image=image)

        return instance



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'discount',
                  'is_active', 'length_type', 'category', 'images', 'created_at', 'updated_at']

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        validated_data['role'] = 'customer'
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='customer'
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
