from django.urls import path
from . import views

urlpatterns = [
    path('edit-subscription/<uuid:subscription_id>/', views.edit_subscription, name='edit_subscription'),
]

