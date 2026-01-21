"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from persons.views import PersonViewSet

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('persons.urls')),
    path('api/', include('webforms.urls')),
    path('api/', include('websites.urls')), 
    
    #path("",include("websites.urls")),
    # Alias per compatibilità Drupal: /contacts → /persons
    path('api/contacts/', PersonViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='contact-list-alias'),
    
    path('api/contacts/<int:pk>/', PersonViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='contact-detail-alias'),
]

