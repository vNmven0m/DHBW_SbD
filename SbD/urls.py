"""SbD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('signout', views.signout, name="signout"),
    path('startpage', views.startpage, name="startpage"),
    path('crshare', views.crshare, name="crshare"),
    path('myshare', views.myshare, name="myshare"),
    path('shshare', views.shshare, name="shshare"),
    path('settings', views.settings, name="settings"),
    path('info', views.info, name="info"),
    path('admin/', admin.site.urls),
    path('permission', views.permission, name="permission"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
