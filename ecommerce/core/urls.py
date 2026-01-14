from django.urls import path
from core import views

urlpatterns  = [
    path('', views.index , name = "index"),
    path('contact', views.contact , name = 'contact'),
    path('about', views.about , name = 'about'),
    path('checkout/',views.checkout,name="Checkout"),
    path('payment-success/', views.payment_success, name='payment_success'),
]

