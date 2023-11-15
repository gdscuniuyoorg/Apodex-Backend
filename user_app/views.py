from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


CustomUser = get_user_model()

class RegisterView(APIView):
   def post(self, request):
       data = json.loads(request.body)
       email = data.get('email')
       password = data.get('password')
       name = data.get('name')

       if email and password and name:
           try:
               user = CustomUser.objects.create_user(email=email, password=password, name=name)
               return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
           except Exception as e:
               return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
       else:
           return Response({'error': 'Email, password, and name are required fields.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
   def post(self, request):
       data = json.loads(request.body)
       email = data.get('email')
       password = data.get('password')

       user = authenticate(request, email=email, password=password)

       if user is not None:
           login(request, user)
           return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
       else:
           return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
   def post(self, request):
       logout(request)
       return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
   def post(self, request):
       if request.user.is_authenticated:
           data = json.loads(request.body)
           request.user.name = data.get('name', request.user.name)
           request.user.save()
           return Response({'message': 'Profile updated successfully!'}, status=status.HTTP_200_OK)
       else:
           return Response({'error': 'User not authenticated.'}, status=status.HTTP_400_BAD_REQUEST)

