from django import forms
from .models import SubscriptionInstance

class SubscriptionEditForm(forms.ModelForm):
    class Meta:
        model = SubscriptionInstance
        fields = ['status', 'start_date', 'end_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }