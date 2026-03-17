from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('application-create/', views.application_create, name='application_create'),
    path('application/', views.application, name='application'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
