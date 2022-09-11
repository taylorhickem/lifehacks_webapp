from django.urls import path

from . import views

app_name = 'hours'
urlpatterns = [
    path('', views.index, name='index'),
    path('refresh/', views.refresh, name='refresh'),
    path('update/', views.update, name='update'),
]