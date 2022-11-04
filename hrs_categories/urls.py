from django.urls import path

from . import views

app_name = 'hrs_categories'
urlpatterns = [
    path('', views.index, name='index'),
    path('roles/', views.RoleListView.as_view(), name='roles'),
    path('role/<int:pk>/', views.RoleDetailView.as_view(), name='role'),
    path('role-update/<int:pk>/', views.RoleUpdateView.as_view(), name='role-update'),
    path('role-delete/<int:pk>/', views.RoleDeleteView.as_view(), name='role-delete'),
    path('role-create/', views.RoleCreateView.as_view(), name='role-create'),
]