from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """
    A Paystack plan available for subscription.
    Amounts are stored in subunits (cents): ZAR 120.00 = 12000.
    """

    INTERVAL_CHOICES = (("monthly", "Monthly"), ("annually", "Annually"))

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(help_text="Subunits (cents). ZAR 120.00 = 12000")
    currency = models.CharField(max_length=3, default="ZAR")
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subscription(models.Model):
    """
    A user's subscription to a plan, mirrored from Paystack webhook events.
    """

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("cancelled", "Cancelled"),
        ("past_due", "Past Due"),
        ("attention", "Attention"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    customer_code = models.CharField(max_length=100)
    subscription_code = models.CharField(max_length=100, unique=True)
    email_token = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_at = models.DateTimeField(null=True)
    next_payment_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    """
    A charge against a subscription, recorded from Paystack webhook events.
    """

    subscription = models.ForeignKey(
        Subscription, null=True, on_delete=models.SET_NULL, related_name="transactions"
    )
    reference = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(help_text="Subunits (cents).")
    currency = models.CharField(max_length=3, default="ZAR")
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(null=True)
    raw = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
