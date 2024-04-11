from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.orders, name='orders'),
    path('orders/<str:order_id>/capture', views.capture, name='capture'),
    path('', views.checkout_page, name='checkout_page'),
]