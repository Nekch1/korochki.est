from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ApplicationCreateForm, RewiewForm
from .models import Application

def index_page(request):
    return render(request, 'index.html')

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_func(request):
    logout(request)
    return redirect('home')


@login_required
def application_create(request):
    if request.method == 'POST':
        form = ApplicationCreateForm(request.POST)
        if form.is_valid():
            course_request = form.save(commit=False)
            course_request.user = request.user
            course_request.save()
            return redirect('home') 
    else:
        form = ApplicationCreateForm()

    return render(request, 'application_create.html', {'form': form})



@login_required
def application(request):
    user_app = Application.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        course_app = get_object_or_404(Application, id=app_id, user=request.user)
        form = RewiewForm(request.POST, instance=course_app)
        if form.is_valid():
            form.save()
            return redirect('my_requests')
    else:
        form = None

    return render(request, 'application.html', {
        'requests': user_app,
        'form': form
    })