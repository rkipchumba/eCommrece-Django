from urllib.parse import urlparse, urlunparse
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Custom is_safe_url function
def is_safe_url(url, allowed_hosts):
    url_info = urlparse(url)
    return (
        not url_info.netloc
        or url_info.netloc in allowed_hosts
        or url_info.netloc == ""
    )

from .forms import LoginForm, RegisterForm

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    print('user logged in')
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or '/'
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            if is_safe_url(redirect_path, [request.get_host()]):  # Use custom is_safe_url
                return redirect(redirect_path)
            else:
                return redirect("/")

            # Redirect to the success page
            # context['form'] = LoginForm()
            return redirect('/')
        else:
            # Return an invalid login message
            print('Error')

    return render(request, 'accounts/login.html', context)

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

    return render(request, 'accounts/login.html', context)
