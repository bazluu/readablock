import json

from django.http import HttpResponse

from ninja import NinjaAPI

from billing import services

api = NinjaAPI(urls_namespace="billing")


@api.post("/webhook/")
def paystack_webhook(request):
    if not services.is_valid_signature(request.body, request.headers.get("x-paystack-signature")):
        return HttpResponse(status=401)

    try:
        event, data = services.parse_event(request.body)
    except (KeyError, json.JSONDecodeError):
        return HttpResponse(status=400)

    # Always acknowledge with 200 so Paystack does not retry the event.
    services.handle_event(event, data)

    return HttpResponse(status=200)
