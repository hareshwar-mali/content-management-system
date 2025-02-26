from rest_framework import serializers
from .models import User, ContentItem, Category
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country',
                  'pincode']

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'author', 'title', 'body', 'summary', 'document', 'categories']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
