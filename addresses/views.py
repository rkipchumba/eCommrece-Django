from django.shortcuts import render, redirect
from urllib.parse import urlparse
from .forms import AddressForm

from billing.models import BillingProfile

def is_safe_url(url, allowed_hosts):
    url_info = urlparse(url)
    if not url_info.netloc or url_info.netloc in allowed_hosts:
        return True
    return False

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or '/'
    
    # Replace 'your_allowed_hosts' with a list of allowed hosts from your project settings.
    allowed_hosts = ['your_allowed_host_here']

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()
        else:
            print('error here')
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, allowed_hosts):
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")
    
    return redirect("cart:checkout")


# def checkout_address_create_view(request):
#     form = AddressForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(request.POST)
#         instance = form.save(commit=False)
#         billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#         if billing_profile is not None:
#             instance.billing_profile = billing_profile
#             instance.address_type = request.POST.get('address_type', 'shipping')
#             instance.save()
#         else:
#             print("Error here")
#             return redirect("cart:checkout")

#         if is_safe_url(redirect_path, request.get_host()):
#             return redirect(redirect_path)
#         else:
#             return redirect("cart:checkout")
#     return redirect("cart:checkout") 