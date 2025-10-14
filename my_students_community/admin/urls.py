# Add these URL patterns to your students/urls.py

from django.contrib import Admins
from django.urls import path, include
from . import views
from .views import Admins_API, AdminsLoginAPI

urlpatterns = [
    # API endpoints (existing)
    path('add/', Admins_API.as_view({'post':'create'})),
    path('all/', Admins_API.as_view({'get':'list'})),
    path('details/<int:pk>/', Admins_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', Admins_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', Admins_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', Admins_API.as_view({'delete':'destroy'})),
    path('login/', AdminsLoginAPI.as_view({'post':'login'})),
    # path('search/', Admins_API.as_view({'post':'search'})),
    
    
]