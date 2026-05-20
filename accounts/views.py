from rest_framework import generics, views, status
from .models import CustomUser, Profile
from .serializers import UserSerializer , ProfileSerializer , EmailSerializer , PasswordChangeSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# User registration endpoint
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()

# User login endpoint
class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        # Check required fields
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Create token for authenticated user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": user.id,
            "email": user.email
        })

# Logout authenticated user
class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"})

# Change user email
class EmailUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user

# Change user password
class PasswordChangeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        # Remove old tokens after password change
        Token.objects.filter(user=user).delete()

        return Response({
            "message": "Password updated successfully"
        })


# Get logged-in user's profile
class ProfileDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


# Update logged-in user's profile
class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.select_related("user").get(user=self.request.user)