from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.password_validation import validate_password


# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password"]

        # Hide password from response
        extra_kwargs = {"password": {"write_only": True}}

    # Validate password using Django validators
    def validate_password(self, value):
        validate_password(value)
        return value

    # Create user with hashed password
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

# Serializer for changing email
class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email"]


# Serializer for changing password
class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
    

# Serializer for user profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "user", "name", "profile_image"]

        # Prevent user field from being updated manually
        read_only_fields = ["user"]