from django.urls import path

from . import views

app_name = 'hours'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('refresh/', views.refresh, name='refresh'),
    path('update/', views.update, name='update'),
]