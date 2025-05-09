# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path('subscriptions/', include('apps.subscriptions.urls')),  # Include subscriptions URLs
    path('', include('apps.home.urls')),             # UI Kits Html files
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),  # Use your custom template
    path('logout/', LogoutView.as_view(), name='logout'),  # Ensure logout is also defined
]
