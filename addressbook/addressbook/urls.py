"""addressbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from django.urls import re_path

from user.views import UserCreate
from contact.views import ContactView, ContactListCreateView, ContactListListCreateView, ContactListView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/users$', UserCreate.as_view()),
    re_path(r'^api/users/tokens$', obtain_jwt_token),
    path(r'api/contacts', ContactListCreateView.as_view()),
    path(r'api/contacts/<int:pk>', ContactView.as_view()),
    path(r'api/contact-lists', ContactListListCreateView.as_view()),
    path(r'api/contact-lists/<int:pk>', ContactListView.as_view())
]
