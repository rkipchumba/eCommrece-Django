from django.shortcuts import render

import stripe
stripe.api_key = "sk_test_51N7Ev4GCBBy71y1GvMTAGNwEC9c689VlZdTCVkWm4jTliTx89h5qzJtDdUC1gEZ3jPUhL7eLWZ7H3H1GJshuYhPL00QWQzC99y"


STRIPE_PUB_KEY = 'pk_test_51N7Ev4GCBBy71y1Gz612DmzcqFfy0lsrzhhFQCwjsMmWJ9rJ5l4UQVHWM5sUtuszwQJdG9dlmuKABULDxzXvgHWf00W14nXBjf'


def payment_method_view(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})