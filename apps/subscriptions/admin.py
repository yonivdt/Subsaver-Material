from django.contrib import admin
from .models import Subscription, SubscriptionInstance

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'category', 'cost', 'luxury')

@admin.register(SubscriptionInstance)
class SubscriptionInstanceAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'subowner', 'status', 'start_date', 'end_date')
