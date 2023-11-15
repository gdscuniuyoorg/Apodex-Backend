from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer, UserRegisterSerializer

class UserRegisterView(APIView):
    """
    View for user registration.

    Allows users to register by providing email, password, and optional name.
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
            serializer.save()
            return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
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
        user = serializer.validated_data['user']
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
        return request.user.profile

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
