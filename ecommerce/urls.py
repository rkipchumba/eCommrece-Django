"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import login_page, register_page, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view 
from carts.views import cart_detail_api_view

from .views import home_page, about_page, contact_page

urlpatterns = [
    path("", home_page, name='home'),
    path("about/", about_page, name='about'),
    path("contact/", contact_page, name='contact'),
    path("login/", login_page, name='login'),
    path("register/guest", guest_register_view, name='guest_register'),
    path("checkout/address/create/", checkout_address_create_view, name='checkout_address_create'),
    path("checkout/address/reuse/", checkout_address_reuse_view, name='checkout_address_reuse'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('cart/', include(('carts.urls', 'carts'), namespace='cart')),
    path("register/", register_page, name='register'),
    path("bootstrap/", TemplateView.as_view(template_name='bootstrap/example.html')), 
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('search/', include(('search.urls', 'search'), namespace='search')),    # path("products/", ProductListView.as_view()),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)