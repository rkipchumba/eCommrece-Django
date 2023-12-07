from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

import stripe
from .models import BillingProfile, Card

stripe.api_key = "sk_test_51N7Ev4GCBBy71y1GvMTAGNwEC9c689VlZdTCVkWm4jTliTx89h5qzJtDdUC1gEZ3jPUhL7eLWZ7H3H1GJshuYhPL00QWQzC99y"
STRIPE_PUB_KEY = 'pk_test_51N7Ev4GCBBy71y1Gz612DmzcqFfy0lsrzhhFQCwjsMmWJ9rJ5l4UQVHWM5sUtuszwQJdG9dlmuKABULDxzXvgHWf00W14nXBjf'

def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if url_has_allowed_host_and_scheme(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})

def payment_method_createview(request):
    print('user making the request: ', request.user)  # Print the user making the request
    print(' POST data: ', request.POST)  # Print the POST data
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print(f"Billing Profile: {billing_profile}, Created: {billing_profile_created}")

        if not billing_profile:
            print("Billing profile not found")
            return JsonResponse({"message": "Billing profile not found"}, status=401)
        
        # Ensure that the billing profile has a customer_id
        if not billing_profile.customer_id:
            print("Billing profile has no customer ID")
            return JsonResponse({"message": "Billing profile has no customer ID"}, status=401)

        token = request.POST.get("token")
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            print(f"Stripe Customer ID: {customer.id}")

            card_response = customer.sources.create(source=token)
            new_card_obj = Card.objects.add_new(billing_profile, card_response)
            print(f"New Card Object: {new_card_obj}")

            # start saving our cards too!
            return JsonResponse({"message": "Success! Your card was added."})
    
    print("Invalid request")
    return JsonResponse({"message": "Invalid request"}, status=400)

