from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from progress.forms import RegistrationForm, SocietyForm, UserEditForm
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
    return HttpResponseRedirect('/dashboard/user')

def user(request):
    if request.GET and request.GET['society']:
        users = CustomUser.objects.filter(society=request.GET['society'])
    else:
        users = CustomUser.objects.all()
    return render(request, 'progress/user_list.html', {'users': users, 'title': 'Users'})

def newuser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Save the User
            form.save()
            return HttpResponseRedirect('/dashboard/user', {'success', 'User Created Successfully'})
        else:
            return render(request, 'progress/newuser.html', {'form': form, 'title': 'Users'})
    else:
        form = RegistrationForm()
        return render(request,'progress/newuser.html', {'form': form, 'title': 'Users'})

def edituser(request, id=None):
    user = CustomUser.objects.get(id=id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/user', {'success': 'User Updated'})
        else:
            return render(request, 'progress/edituser.html', {'id': user.id, 'form': form, 'title': 'Users'})
    else:
        form = UserEditForm(instance=user)
        return render(request,'progress/edituser.html', {'id': user.id, 'form': form, 'title': 'Users'})

def society(request):
    societies = Society.objects.all()
    return render(request, 'progress/society_list.html', {'societies': societies, 'title': 'Societies'})

def newsociety(request):
    if request.method == "POST":
        form = SocietyForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/society', {'success': 'Society Added'})
        else:
            return render(request, 'progress/newsociety.html', {'form': form, 'title': 'Societies'})
    else:
        form = SocietyForm()
        return render(request, 'progress/newsociety.html', {'form': form, 'title': 'Societies'})

def editsociety(request, id=None):
    society = Society.objects.get(id=id)
    if request.method == "POST":
        form = SocietyForm(request.POST, instance=society)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/society', {'success': 'Society Updated'})
        else:
            return render(request, 'progress/editsociety.html', {'id': society.id, 'form': form, 'title': 'Societies'})
    else:
        form = SocietyForm(instance=society)
        return render(request,'progress/editsociety.html', {'id': society.id, 'form': form, 'title': 'Societies'})
