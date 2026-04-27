from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Vue d'Inscription (déjà faite)
    path('register_merchant/', views.register_merchant_view, name='register_merchant'),
    path('register/success/', views.registration_success_view, name='registration_success'),
    
    # 🚨 Vue de Connexion (Utilise login.html) 🚨
    path('login/', views.login_merchant_view, name='merchant_login'), 
    
    # 🚨 Vue de Tableau de Bord (Utilise dashboard.html) 🚨
    path('dashboard/', views.dashboard_view, name='merchant_dashboard'),
    path('dashboard/export-csv/', views.export_transactions_csv, name='export_transactions_csv'),
    
    # Profile management
    path('profile/', views.profile_view, name='merchant_profile'),
    
    # API endpoints
    path('api/', views.api_view, name='merchant_api'),
    path('api/demo-live/', views.demo_boutique, name='demo_boutique'),
    
    # Logout
    path('logout/', views.logout_merchant_view, name='merchant_logout'),


    # 1. Demande d'email
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='merchant/password_reset_form.html'
    ), name='password_reset'),

    # 2. Confirmation d'envoi
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='merchant/password_reset_done.html'
    ), name='password_reset_done'),

    # 3. Lien cliqué dans l'email (changement du mot de passe)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='merchant/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # 4. Succès final
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='merchant/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('profile/delete/', views.delete_account_view, name='delete_account'),
]