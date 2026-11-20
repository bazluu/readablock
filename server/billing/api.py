import json

from django.http import HttpResponse

from ninja import NinjaAPI
from ninja.responses import Response

from billing import services

api = NinjaAPI(urls_namespace="billing")


@api.get("/status/")
def billing_status(request):
    try:
        user_id = request.session["user_id"]
    except KeyError:
        return Response({"error": "Authentication required"}, status=401)

    return Response({"entitled": services.is_entitled(user_id)}, status=200)


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
