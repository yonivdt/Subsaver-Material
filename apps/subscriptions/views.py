from django.shortcuts import render, get_object_or_404, redirect
from .models import SubscriptionInstance
from .forms import SubscriptionEditForm

def edit_subscription(request, subscription_id):
    subscription = get_object_or_404(SubscriptionInstance, id=subscription_id, subowner=request.user)

    if request.method == 'POST':
        form = SubscriptionEditForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('my_subscriptions')  # Redirect back to the subscriptions page
    else:
        form = SubscriptionEditForm(instance=subscription)

    return render(request, 'subscriptions/edit_subscription.html', {'form': form, 'subscription': subscription})
