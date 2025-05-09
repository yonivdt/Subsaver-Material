from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
import uuid # Required for unique subscription instances
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from datetime import date, timedelta

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Company(models.Model):
    """Model representing an company."""
    name = models.CharField(max_length=200, unique=True, help_text="Name of a company that supplies a subscription service")

    def __str__(self):
            """String for representing the Model object."""
            return f'{self.name}'

    def get_absolute_url(self):
        """Returns the URL to access a particular company instance."""
        return reverse('company-detail', args=[str(self.id)])
    class Meta:
        ordering = ['name']
    
class Subscription(models.Model):
    """A Model representing a subscription type"""
    # Fields
    name = models.CharField(max_length=200, help_text='Name of a Subscription',)
    company = models.ForeignKey('Company', on_delete=models.RESTRICT, help_text='Parent company of the subscription', null=True)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, help_text='Category of the subscription', default=1)
    description = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter a brief description of the subscription",)
    cost = models.DecimalField(max_digits=5, decimal_places=2, help_text='cost of a subscription', default=Decimal(0),)
    yearlysavings = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0), validators=PERCENTAGE_VALIDATOR, help_text='Savings percentage when taking a subscription for 12 months',)
    luxury = models.BooleanField(default=True, help_text='Is this a luxury subscription?')

    def __str__(self):
        """String for representing the Subscription object (in Admin site etc.)."""
        return f'{self.name}'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this subscription."""
        return reverse('subscription-detail', args=[str(self.id)])

class UserSubscriptionInstanceManager(models.Manager):
    def get_queryset(self, user):
        return super().get_queryset().filter(subowner=user)


class SubscriptionInstance(models.Model):
    """Model representing a specific subscription (i.e. a customers' subscription)."""
    SUBSCRIPTION_STATUS = [
    ('a', 'Active'),
    ('d', 'Disabled'),
    ('p', 'Planned to start'),
    ('e', 'Planned to end'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular subscription - which will be owned by a user",)
    subscription = models.ForeignKey('Subscription', on_delete=models.RESTRICT, null=True, help_text='The subscription that this instance is for',)
    start_date = models.DateField(blank=True, help_text='Start date of the subscription', null=True)
    duration = models.DurationField(null=True, blank=True, help_text='Duration of the subscription',)
    end_date = models.DateField(blank=True, help_text='End Date of the subscription', null=True)
    country = CountryField(default="BE", blank=False, blank_label="(select country)", )
    sub_username = models.CharField(max_length=1024, blank=True, null=True)
    sub_password = models.CharField(max_length=1024, blank=True, null=True)
    subowner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, help_text='The user that owns this subscription',)
    status = models.CharField(max_length=1, choices=SUBSCRIPTION_STATUS, blank=True, default='d', help_text='Subscription active, inactive or planned to start, or planned to end',)

    objects = models.Manager() # The default manager.
    user_subs = UserSubscriptionInstanceManager() # The user-specific manager.

    @property
    def is_ending_soon(self):
        """Returns True if the subscription is ending within 7 days"""
        return bool(self.end_date and self.end_date <= date.today() + timedelta(days=7))
    
    @property
    def days_remaining(self):
        """Returns the number of days remaining until the subscription ends"""
        if self.end_date:
            return (self.end_date - date.today()).days
        return None
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.subscription.name})'
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this subscriptioninstance."""
        return reverse('subscriptioninstance-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['end_date']
        permissions = (("Do not renew", "Set subscription to not be renewed at end date"),)

class Category(models.Model):
    """Model representing a Category that a subscription can belong to"""
    name = models.CharField(max_length=200, unique=True, help_text="We'll want to be able to group subscriptions based on the category they belong to",)

    def get_absolute_url(self):
        """Returns the URL to access a particular category instance."""
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

class SubsaverUser(models.Model):
    """Model representing a user of the subsaver site"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    subsaver_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular user",)
    subsaver_username = models.CharField(max_length=1024, blank=True)
    subsaver_password = models.CharField(max_length=1024, blank=True)
    subsaver_email = models.EmailField(max_length=1024, blank=True)
    subsaver_country = CountryField(default="BE", blank=False, blank_label="(select country)", )
    subsaver_subscription = models.ManyToManyField(SubscriptionInstance, help_text="Subscriptions that this user has",)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.subsaver_username}'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this user."""
        return reverse('subsaverusers-detail', args=[str(self.subsaver_id)])
    
    class Meta:
        ordering = ['subsaver_username']
        permissions = (("Can add subscription", "Can add a subscription to the user"),)