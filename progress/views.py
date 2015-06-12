from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from progress.forms import RegistrationForm, SocietyForm, UserEditForm , TaskForm
from progress.models import CustomUser, Society , Task

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

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def dashboard(request):
    return HttpResponseRedirect('/dashboard/user')

@login_required
def user(request):
    if request.GET and request.GET['society']:
        users = CustomUser.objects.filter(society=request.GET['society'])
    else:
        users = CustomUser.objects.all()
    return render(request, 'progress/user_list.html', {'users': users, 'title': 'Users'})

@login_required
def newuser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Save the User
            instance = form.save(commit=False)
            instance.password = make_password(form.cleaned_data['password'])
            instance.save()
            return HttpResponseRedirect('/dashboard/user', {'success', 'User Created Successfully'})
        else:
            return render(request, 'progress/newuser.html', {'form': form, 'title': 'Users'})
    else:
        form = RegistrationForm()
        return render(request,'progress/newuser.html', {'form': form, 'title': 'Users'})

@login_required
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

@login_required
def society(request):
    societies = Society.objects.all()
    return render(request, 'progress/society_list.html', {'societies': societies, 'title': 'Societies'})

@login_required
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

@login_required
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

@login_required
def task(request):
    tasks = Task.objects.all()
    return render(request, 'progress/tasks_list.html', {'tasks': tasks, 'title': 'Task'})

@login_required
def newtask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect('/dashboard/task', {'success': 'Task Added'})
        else:
            return render(request, 'progress/newtask.html', {'form': form, 'title': 'Task'})    
    else:
        form = TaskForm()
        return render(request, 'progress/newtask.html', {'form': form, 'title': 'Task'})


@login_required
def edittask(request, id=None):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/task', {'success': 'Task Updated'})
        else:
            return render(request, 'progress/edittask.html', {'id': task.id, 'form': form, 'title': 'Task'})
    else:
        form = TaskForm(instance=task)
        return render(request,'progress/edittask.html', {'id': task.id, 'form': form, 'title': 'Task'})