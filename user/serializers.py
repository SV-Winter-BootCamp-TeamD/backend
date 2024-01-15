from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'user_email', 'user_name', 'user_password']

    def create(self, validated_data):
        return User.objects.create_user(
            user_email=validated_data['user_email'],
            user_name=validated_data['user_name'],
            user_password=validated_data['user_password']
        )

class UserLoginSwaggerSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'user_email', 'user_password']

    def create(self, validated_data):
        return User.objects.create_user(
            user_email=validated_data['user_email'],
            user_password=validated_data['user_password']
        )