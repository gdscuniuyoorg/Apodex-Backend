from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

CustomUser = get_user_model()

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if email and password and name:
            try:
                user = CustomUser.objects.create_user(email=email, password=password, name=name)
                return JsonResponse({'message': 'User registered successfully!'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Email, password, and name are required fields.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful!'})
        else:
            return JsonResponse({'error': 'Invalid email or password.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful!'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            request.user.name = data.get('name', request.user.name)
            request.user.save()
            return JsonResponse({'message': 'Profile updated successfully!'})
        else:
            return JsonResponse({'error': 'User not authenticated.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
