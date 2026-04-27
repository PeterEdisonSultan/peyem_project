# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # L'API (sera accessible via payment/api/initiate/)
    path('api/initiate/', views.api_initiate_payment, name='api_initiate_payment'),

    # Checkout (sera accessible via payment/checkout/...)
    path('checkout/<uuid:reference_id>/', views.checkout_view, name='checkout_view'),

    # Simulation (sera accessible via payment/simulate/...)
    # IMPORTANT: J'ai retiré le 'payment/' ici pour éviter le doublon payment/payment/
    path('simulate/<uuid:reference_id>/<str:provider>/', views.simulate_provider_view, name='simulate_provider'),

    # Succès
    path('success/<uuid:reference_id>/', views.payment_success_view, name='payment_success'),

    path('api/check-status/', views.api_check_status, name='api_check_status'),
]