from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm, ApplicationCreateForm, RewiewForm
from .models import Application
from django.http import HttpResponseForbidden

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
            return redirect('application')
    else:
        form = None

    return render(request, 'application.html', {
        'applications': user_app,
        'form': form
    })


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('home') 

    # Фильтрация по статусу через GET-параметр
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = Application.objects.filter(status=status_filter).order_by('-created_at')
    else:
        applications = Application.objects.all().order_by('-created_at')

    # Пагинация
    paginator = Paginator(applications, 10)  # 10 заявок на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_panel.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': Application.STATUS_CHOICES
    })


@login_required
def change_status(request, app_id):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        app = get_object_or_404(Application, id=app_id)
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES).keys():
            app.status = new_status
            app.save()

    return redirect('admin_panel')