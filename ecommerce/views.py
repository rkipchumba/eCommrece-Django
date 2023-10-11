import email
from django.contrib.auth import authenticate, login, get_user_model
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    context = {
        'title': 'Hello, World!',
        'content': 'Welcome to the Home Page',
        
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'Yeaahhh im premium'
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
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == 'POST':
    #     # print(request.POST)
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))


    return render(request, 'contact/view.html', context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print('user logged in')
    # print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        # print(request.user.is_authenticated)
    
        if user is not None:
            # print(request.user.is_authenticated)
            login(request, user)  # Updated login function call
            # Redirect to success page
            # context['form'] = LoginForm()
            return redirect('/')
        else:
            # Return invalid login message
            print('Error')

    return render(request, 'auth/login.html', context)

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username, email, password)
        print(new_user)


    return render(request, 'auth/login.html', context)