# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from apps.subscriptions.models import SubscriptionInstance

def index(request):
    # Get the user's active subscriptions if logged in
    if request.user.is_authenticated:
        active_subscriptions = SubscriptionInstance.objects.filter(subowner=request.user, status='a')
        total_active_subscriptions = active_subscriptions.count()
        total_monthly_cost = sum(subscription.subscription.cost for subscription in active_subscriptions)
    else:
        active_subscriptions = []
        total_active_subscriptions = 0
        total_monthly_cost = 0

    # Pass the total number of active subscriptions to the template
    context = {
        'segment': 'index',
        'total_active_subscriptions': total_active_subscriptions,
        'total_monthly_cost': total_monthly_cost,
    }

    return render(request, 'home/index.html', context)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        # Prevent processing of invalid templates
        if load_template in ['login', 'admin']:
            return HttpResponseRedirect(reverse('index'))  # Redirect to the index page instead

        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def my_subscriptions(request):
    # Fetch the user's subscriptions
    user_subscriptions = SubscriptionInstance.objects.filter(subowner=request.user)

    # Pass the subscriptions to the template
    context = {
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'home/MySubscriptions.html', context)
