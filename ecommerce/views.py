import email
from django.contrib.auth import authenticate, login, get_user_model
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def home_page(request):
    # print(request.session.get('first_name', "Unknown")) #Get
    context = {
        'title': 'Hello, World!',
        'content': 'Welcome to the Shop Home Page',
        
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'Premium Customer'
    return render(request, 'home_page.html', context)

def about_page(request):
    context = {
        'title': 'About Page',
        'content': 'Welcome to the About Page'
    }
    return render(request, 'home_page.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact Page',
        'content': 'Welcome to the Contact Page',
        'form': contact_form,
    }

    if request.method == 'POST': 
        if contact_form.is_valid():
            # Form is valid, you can proceed with processing the data.
            print(contact_form.cleaned_data)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                message = "Thank you for your submission"
                response_data = {'message': message}  # Create a dictionary with a "message" key
                return JsonResponse(response_data, safe=False)  # Return a JsonResponse with the dictionary
        else:
            # Form has errors, return validation errors as JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = contact_form.errors.as_json()
                return JsonResponse(errors, status=400)


    return render(request, 'contact/view.html', context)

