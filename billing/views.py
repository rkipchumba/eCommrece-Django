from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import django

if django.VERSION >= (4, 0):
    from django.utils.http import url_has_allowed_host_and_scheme

    def is_safe_url(url, allowed_hosts=None):
        return url_has_allowed_host_and_scheme(url, allowed_hosts)
else:
    from django.utils.http import is_safe_url

import stripe
stripe.api_key = "sk_test_51N7Ev4GCBBy71y1GvMTAGNwEC9c689VlZdTCVkWm4jTliTx89h5qzJtDdUC1gEZ3jPUhL7eLWZ7H3H1GJshuYhPL00QWQzC99y"

STRIPE_PUB_KEY= 'pk_test_51N7Ev4GCBBy71y1Gz612DmzcqFfy0lsrzhhFQCwjsMmWJ9rJ5l4UQVHWM5sUtuszwQJdG9dlmuKABULDxzXvgHWf00W14nXBjf'

from .models import BillingProfile

def payment_method_view(request):
    # if request.user.is_authenticated:
        # Indent the code block after the if statement by one level.
        # billing_profile = request.user.billingprofile
        # my_customer_id = billing_profile.customer_id
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            print(card_response) # start saving our cards too!
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
