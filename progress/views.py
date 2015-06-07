from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import auth
from progress.models import CustomUser, Society

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

def dashboard(request): 
    return render(request, 'progress/dashboard.html')

def newuser(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        society =  request.POST.get('society', '')
        position =  request.POST.get('position', '')
        role =  request.POST.get('role', '')
        gender =  request.POST.get('gender', '')
        contact =  request.POST.get('contact', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        nominated_on = request.POST.get('nominated_on', '')
        nominated_through = request.POST.get('nominated_through', '')

        s = Society.objects.get(pk=society)

        user = CustomUser.object.create(
            first_name=first_name,
            last_name=last_name,    
            password=password,
            email=email,
            society=s,
            position=position,
            role=role,
            gender=gender.
            contact_number=contact,
            date_of_birth=dob,
            nominated_on=nominated_on,
            nominated_through=nominated_through
        )

        user.save()
        return HttpResponseRedirect('/dashboard', {'success', 'User Created Successfully'})
    else:
        societies = Society.objects.all()
        return render(request,'progress/newuser.html', {'societies': societies})