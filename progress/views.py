from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from progress.models import CustomUser

# Create your views here.

def index(request):
    return render(request, 'progress/index.html')

def login(request):
    # if user is logged in then redirect to the dashboard

    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active:
            # Login the user
            auth.login(request, user)
            return JsonResponse({'message': 'Login Successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid Username/Password'}, status=500)
    return render(request, 'progress/login.html')
