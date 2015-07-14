from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from progress.filters import CustomUserFilter, NewsFilter, TaskAdminFilter, TaskFilter
from progress.forms import NewsForm, RegistrationForm, SocietyForm, UserEditForm , TaskForm
from progress.models import CustomUser, News, Society, Task

# Create your views here.

def index(request):
    news = News.objects.all().order_by('-created_on')[:5]
    return render(request, 'progress/index.html', {'news': news})

def login(request):
    # if user is logged in then redirect to the dashboard
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')

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
    return HttpResponseRedirect('/dashboard/task')

@login_required
def user(request):
    filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all().order_by('first_name', 'last_name'))
    fields = request.user._meta.get_all_field_names()
    return render(request, 'progress/user_list.html', {'filter': filter, 'title': 'Users', 'curr_user': request.user, 'fields': fields})

@login_required
def newuser(request):
    group = request.user.groups.get()
    if group.name == 'SC' or group.name == 'Administrator':
        if request.method == "POST":
            if group.name == 'Administrator':
                form = RegistrationForm(request.POST, request.FILES, admin=True)
            else:
                form = RegistrationForm(request.POST, request.FILES, admin=False)

            if form.is_valid():
                # Save the User
                form.save()
                return HttpResponseRedirect('/dashboard/user', {'success', 'User Created Successfully'})
            else:
                return render(request, 'progress/newuser.html', {'form': form, 'title': 'Users'})
        else:
            if group.name == 'Administrator':
                form = RegistrationForm(admin=True)
            else:
                form = RegistrationForm(admin=False)
            return render(request,'progress/newuser.html', {'form': form, 'title': 'Users'})
    else:
        return HttpResponseRedirect('/dashboard/user')

@login_required
def edituser(request, id=None):
    user = CustomUser.objects.get(id=id)
    group = request.user.groups.get()
    if group.name == 'SC' or group.name == 'Administrator' or user.pk == request.user.pk:
        if request.method == "POST":
            if group.name == 'Administrator':
                form = UserEditForm(request.POST, request.FILES, instance=user, admin=True)
            else:
                form = UserEditForm(request.POST, request.FILES, instance=user, admin=False)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/user', {'success': 'User Updated'})
            else:
                return render(request, 'progress/edituser.html', {'id': user.id, 'form': form, 'title': 'Users'})
        else:
            if group.name == 'Administrator':
                form = UserEditForm(instance=user, admin=True)
            else:
                form = UserEditForm(instance=user, admin=False)
            return render(request,'progress/edituser.html', {'id': user.id, 'form': form, 'title': 'Users'})
    return HttpResponseRedirect('/dashboard/user')

@login_required
def printuser(request):
    group = request.user.groups.get()
    filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.all().order_by('first_name', 'last_name'))
    fields = request.POST.dict()
    remove = ['action', 'csrfmiddlewaretoken', 'password']
    for entry in remove:
        if entry in fields:
            del fields[entry]

    return render(request, 'progress/printuser.html', {'filter': filter, 'fields': fields})

@login_required
def society(request):
    societies = Society.objects.all().order_by('name')
    s = Society()
    fields = s.fields()
    return render(request, 'progress/society_list.html', {'societies': societies, 'title': 'National Societies', 'fields': fields})

@login_required
def newsociety(request):
    group = request.user.groups.get()

    if group.name == 'SC' or group.name == 'Administrator':
        if request.method == "POST":
            form = SocietyForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/society', {'success': 'Society Added'})
            else:
                return render(request, 'progress/newsociety.html', {'form': form, 'title': 'National Societies'})
        else:
            form = SocietyForm()
            return render(request, 'progress/newsociety.html', {'form': form, 'title': 'National Societies'})
    return HttpResponseRedirect('/dashboard/society')

@login_required
def editsociety(request, id=None):
    society = Society.objects.get(id=id)
    group = request.user.groups.get()

    if group.name == 'SC' or group.name == 'Administrator' or request.user.society == society:
        if request.method == "POST":
            form = SocietyForm(request.POST, instance=society)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/society', {'success': 'Society Updated'})
            else:
                return render(request, 'progress/editsociety.html', {'id': society.id, 'form': form, 'title': 'National Societies'})
        else:
            form = SocietyForm(instance=society)
            return render(request,'progress/editsociety.html', {'id': society.id, 'form': form, 'title': 'National Societies'})
    return HttpResponseRedirect('/dashboard/society')

@login_required
def printsociety(request):
    societies = Society.objects.all().order_by('name')
    fields = request.POST.dict()
    del fields['action']
    del fields['csrfmiddlewaretoken']
    print(fields)
    return render(request, 'progress/printsociety.html', {'filter': societies, 'fields': fields})

@login_required
def task(request):
    group = request.user.groups.get()

    if group.name == 'SC' or group.name == 'Administrator' or 'CC' in group.name:
        filter = TaskAdminFilter(request.GET, queryset=Task.objects.all())
    else:
        filter = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))

    t = Task()
    fields = t.fields()
    return render(request, 'progress/tasks_list.html', {'filter': filter, 'title': 'Tasks', 'fields': fields})

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
        return render(request, 'progress/newtask.html', {'form': form, 'title': 'Tasks'})


@login_required
def edittask(request, id=None):
    task = Task.objects.get(id=id)
    group = request.user.groups.get()

    if group.name == 'SC' or group.name == 'Administrator' or request.user == task.user:
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/task', {'success': 'Task Updated'})
            else:
                return render(request, 'progress/edittask.html', {'id': task.id, 'form': form, 'title': 'Task'})
        else:
            form = TaskForm(instance=task)
            return render(request,'progress/edittask.html', {'id': task.id, 'form': form, 'title': 'Tasks'})
    return HttpResponseRedirect('/dashboard')

@login_required
def printtask(request):
    group = request.user.groups.get()

    if group.name == 'SC' or group.name == 'Administrator' or 'CC' in group.name:
        filter = TaskAdminFilter(request.GET, queryset=Task.objects.all())
    else:
        filter = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))

    fields = request.POST.dict()
    del fields['action']
    del fields['csrfmiddlewaretoken']

    if group.name == "Other":
        del fields['user']

    return render(request, 'progress/printtask.html', {'filter': filter, 'fields': fields})

@login_required
def news(request):
    group = request.user.groups.get()

    if not group.name == 'Administrator':
        return HttpResponseRedirect('/dashboard/task')

    filter = NewsFilter(request.GET, queryset=News.objects.all())

    return render(request, 'progress/news_list.html', {'filter': filter, 'title': 'News'})

@login_required
def newnews(request):
    group = request.user.groups.get()

    if not group.name == 'Administrator':
        return HttpResponseRedirect('/dashboard/task')

    if request.method == 'POST':
        form = NewsForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect('/dashboard/news')
        else:
            return render(request, 'progress/newnews.html', {'form': form, 'title': 'News'})
    else:
        form = NewsForm()
        return render(request, 'progress/newnews.html', {'form': form, 'title': 'News'})

@login_required
def editnews(request, id=None):
    instance = News.objects.get(id=id)
    group = request.user.groups.get()

    if not group.name == 'Administrator':
        return HttpResponseRedirect('/dashboard/task')

    if request.method == 'POST':
        form = NewsForm(request.POST, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect('/dashboard/news')
        else:
            return render(request, 'progress/editnews.html', {'form': form, 'title': 'News', 'id': id})
    else:
        form = NewsForm(instance=instance)
        return render(request, 'progress/editnews.html', {'form': form, 'title': 'News', 'id': id})

@login_required
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/dashboard/user')
        else:
            return render(request, 'progress/changepassword.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'progress/changepassword.html', {'form': form})
