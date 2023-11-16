from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer, UserRegisterSerializer

from django.contrib.auth import authenticate

class UserRegisterView(APIView):
    """
    View for user registration.

    Allows users to register by providing email and password.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A Response indicating success or failure of the registration.
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()
            return Response({
                'detail': 'User registered successfully',
                'user_data': user_data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    View for user login.

    Allows users to log in by providing their email and password.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A Response containing the access and refresh tokens upon successful login.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = authenticate(request, email=email, password=serializer.validated_data['password'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    """
    View for user logout.

    Allows users to log out by providing their refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user logout.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A Response indicating success or failure of the logout.
        """
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
                return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Refresh token is required for logout'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    """
    View for updating user profile.

    Allows authenticated users to view and update their profile information.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        """
        Get the user profile object associated with the authenticated user.

        Parameters:
        - `request`: The HTTP request object.

        Returns:
        - The user profile object.
        """
        return request.user.userprofile

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for retrieving user profile.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A Response containing the user profile data.
        """
        profile = self.get_object(request)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests for updating user profile.

        Parameters:
        - `request`: The HTTP request object.
        - `args`: Additional arguments passed to the view.
        - `kwargs`: Additional keyword arguments passed to the view.

        Returns:
        - A Response containing the updated user profile data.
        """
        profile = self.get_object(request)
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        profile = request.user.userprofile
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API view to retrieve details of the user profile.

    Requires authentication for access.
    """
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Access the UserProfile from the CustomUser instance
        profile = request.user.userprofile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

