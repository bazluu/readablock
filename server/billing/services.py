import hashlib
import hmac
import json
from datetime import datetime, timezone as dt_timezone

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from billing import models

VALID_SUBSCRIPTION_STATUSES = {choice for choice, _ in models.Subscription.STATUS_CHOICES}


def is_valid_signature(raw_body: bytes, signature: str | None) -> bool:
    """
    Paystack signs every webhook payload with HMAC-SHA512 using the secret key,
    sent in the x-paystack-signature header.
    """
    secret = settings.PAYSTACK_SECRET_KEY
    if not secret or not signature:
        return False

    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha512).hexdigest()

    return hmac.compare_digest(expected, signature)


def parse_event(raw_body: bytes) -> tuple[str, dict]:
    payload = json.loads(raw_body)

    return payload["event"], payload.get("data") or {}


def handle_event(event: str, data: dict) -> None:
    handlers = {
        "charge.success": handle_charge_success,
        "subscription.create": handle_subscription_create,
        "invoice.update": handle_invoice_update,
        "subscription.not_renewing": handle_subscription_not_renewing,
        "subscription.disable": handle_subscription_disabled,
    }

    handler = handlers.get(event)
    if handler is None:
        print(f"Ignoring Paystack event: {event}")
        return

    handler(data)


def parse_paystack_datetime(value):
    if not value:
        return None

    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=dt_timezone.utc)

    return parse_datetime(value)


def resolve_user(data: dict):
    email = (data.get("customer") or {}).get("email")

    return User.objects.filter(email=email).first() if email else None


def resolve_plan(plan_data: dict | None):
    """
    Plans are seeded locally, but fall back to creating one from the webhook
    payload so plans added on the Paystack dashboard without a local seed still
    resolve.
    """
    code = (plan_data or {}).get("plan_code")
    if not code:
        return None

    plan, _ = models.Plan.objects.get_or_create(
        code=code,
        defaults={
            "name": plan_data.get("name") or code,
            "amount": plan_data.get("amount") or 0,
            "currency": plan_data.get("currency") or "ZAR",
            "interval": plan_data.get("interval") or "monthly",
        },
    )

    return plan


def upsert_subscription(data: dict, status: str | None = None) -> None:
    """
    Create or update a Subscription from a subscription webhook payload.
    The payload's own status wins unless an explicit status override is passed.
    A payload without customer or plan can only update an existing subscription.
    """
    code = data.get("subscription_code")
    if not code:
        print("Paystack webhook: subscription payload missing subscription_code")
        return

    subscription = models.Subscription.objects.filter(subscription_code=code).first()
    if subscription is None:
        user = resolve_user(data)
        plan = resolve_plan(data.get("plan"))

        if user is None or plan is None:
            print(f"Paystack webhook: no matching user or plan for subscription {code}")
            return

        subscription = models.Subscription(subscription_code=code, user=user, plan=plan)
        subscription.customer_code = (data.get("customer") or {}).get("customer_code", "")
        subscription.email_token = data.get("email_token", "")

    payload_status = data.get("status")
    if status is None and payload_status in VALID_SUBSCRIPTION_STATUSES:
        status = payload_status
    if status is None:
        status = "active"

    subscription.status = status
    subscription.start_at = parse_paystack_datetime(data.get("createdAt")) or subscription.start_at
    subscription.next_payment_at = (
        parse_paystack_datetime(data.get("next_payment_date")) or subscription.next_payment_at
    )
    subscription.cancelled_at = parse_paystack_datetime(data.get("cancelled_at")) or (
        timezone.now() if status == "cancelled" else subscription.cancelled_at
    )
    subscription.save()


def handle_subscription_create(data: dict) -> None:
    upsert_subscription(data)


def handle_subscription_not_renewing(data: dict) -> None:
    # The customer opted out; the plan model has no "not renewing" state, so the
    # subscription is treated as inactive from this point.
    upsert_subscription(data, status="inactive")


def handle_subscription_disabled(data: dict) -> None:
    upsert_subscription(data, status="cancelled")


def handle_invoice_update(data: dict) -> None:
    code = data.get("subscription")
    if not code:
        return

    subscription = models.Subscription.objects.filter(subscription_code=code).first()
    if subscription is None:
        print(f"Paystack webhook: no subscription for invoice update {data.get('invoice_code')}")
        return

    # The payload's status can be an invoice status ("success", "failed") rather
    # than a subscription status, so only apply known subscription statuses.
    if data.get("status") in VALID_SUBSCRIPTION_STATUSES:
        subscription.status = data["status"]

    next_payment_at = parse_paystack_datetime(data.get("next_payment_date"))
    if next_payment_at:
        subscription.next_payment_at = next_payment_at

    subscription.save()


def handle_charge_success(data: dict) -> None:
    subscription = None
    sub_data = data.get("subscription")
    code = sub_data.get("subscription_code") if isinstance(sub_data, dict) else sub_data

    if code:
        subscription = models.Subscription.objects.filter(subscription_code=code).first()
        # A successful charge recovers a subscription that missed payments.
        if subscription and subscription.status in ("past_due", "attention"):
            subscription.status = "active"
            subscription.save()

    models.Transaction.objects.update_or_create(
        reference=data["reference"],
        defaults={
            "subscription": subscription,
            "amount": data["amount"],
            "currency": data.get("currency", "ZAR"),
            "status": data.get("status", "success"),
            "paid_at": parse_paystack_datetime(data.get("paid_at")),
            "raw": data,
        },
    )
