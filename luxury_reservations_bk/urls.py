"""
URL configuration for luxury_reservations_bk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from api.views import CustomTokenCreateView
from api.views import *

def redirect_to_api(request):
    return HttpResponseRedirect('/api/')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', redirect_to_api), 
    path('api/', include('api.urls')),
    path('api/token/login/', CustomTokenCreateView.as_view(), name='custom-token-create'),
    path('api/token/logout/', LogoutView.as_view()),
]
