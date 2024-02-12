from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('status', views.status, name='status'),
    path('welcome', views.welcome, name='index'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('password', views.password, name='password'),
    path('activate/<uidb64>/<token>', views.ActivateView.as_view(), name='activate'),
]
