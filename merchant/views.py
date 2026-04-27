from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import json
import uuid  
import csv
from django.http import HttpResponse
from django.template.loader import render_to_string

from .forms import UserRegistrationForm, MerchantDetailsForm
from .models import MerchantProfile
from payments.models import Transaction

# --- 1. INSCRIPTION (VERSION ROBUSTE) ---
def register_merchant_view(request):
    # Si on est déjà connecté, on va au dashboard
    if request.user.is_authenticated:
        return redirect('merchant_dashboard')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        details_form = MerchantDetailsForm(request.POST)

        if user_form.is_valid() and details_form.is_valid():
            try:
                # 1. On crée l'utilisateur
                email = user_form.cleaned_data['email']
                password = user_form.cleaned_data['password']
                
                # Vérifie si l'utilisateur existe déjà pour éviter le crash
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Cet email est déjà utilisé.")
                    return render(request, 'merchant/register_merchant.html', {'user_form': user_form, 'details_form': details_form})

                user = User.objects.create_user(username=email, email=email, password=password)

                # 2. On crée le profil marchand
                details = details_form.cleaned_data
                
                # Gestion sécurisée des cases à cocher (payment_methods)
                # On assume que c'est une liste. Si c'est vide, on met une liste vide.
                methods = details.get('payment_methods', [])
                if methods is None: methods = []

                MerchantProfile.objects.create(
                    user=user,
                    company_name=details['company_name'],
                    phone=details['phone'],
                    address=details['address'],
                    
                    # Génération automatique de la clé API ici pour être sûr
                    api_key=str(uuid.uuid4()), 
                    
                    accepts_natcash=('natcash' in methods),
                    natcash_name=details.get('natcash_name', ''),
                    natcash_number=details.get('natcash_number', ''),
                    
                    accepts_moncash=('moncash' in methods),
                    moncash_name=details.get('moncash_name', ''),
                    moncash_number=details.get('moncash_number', ''),
                )

                # 3. Connexion automatique après inscription
                login(request, user)
                return redirect('merchant_dashboard')

            except Exception as e:
                # En cas d'erreur, on supprime l'user pour ne pas bloquer l'email
                if 'user' in locals() and user:
                    user.delete()
                print(f"ERREUR INSCRIPTION : {e}") # Regarde ton terminal si ça plante !
                messages.error(request, f"Une erreur est survenue : {e}")

    else:
        user_form = UserRegistrationForm()
        details_form = MerchantDetailsForm()

    return render(request, 'merchant/register_merchant.html', {
        'user_form': user_form, 
        'details_form': details_form
    })

def registration_success_view(request):
    return render(request, 'merchant/registration_success.html')


# --- 2. CONNEXION ---
def login_merchant_view(request):
    if request.user.is_authenticated:
        return redirect('merchant_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('merchant_dashboard')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'merchant/login.html', {'form': form})


# --- 3. DÉCONNEXION ---
def logout_merchant_view(request):
    logout(request)
    return redirect('merchant_login')


# --- 4. DASHBOARD (SÉCURISÉ) ---
@login_required(login_url='merchant_login')
def dashboard_view(request):
    try:
        merchant = MerchantProfile.objects.get(user=request.user)
    except MerchantProfile.DoesNotExist:
        logout(request)
        return redirect('merchant_login')

    transactions = Transaction.objects.filter(merchant=merchant).order_by('-created_at')

    # Calcul revenus
    revenue = 0
    for t in transactions:
        # On vérifie si le statut est valide (Majuscule ou minuscule)
        if str(t.status).upper() in ['SUCCESS', 'COMPLETED']:
            revenue += float(t.amount)

    # Données Graphique
    today = timezone.now().date()
    graph_labels = []
    graph_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = transactions.filter(created_at__date=day).count()
        graph_labels.append(day.strftime("%d/%m"))
        graph_data.append(count)

    context = {
        'merchant': merchant,
        'nom_entreprise': merchant.company_name,
        'transactions': transactions,
        'stats': {
            'total': transactions.count(),
            'pending': transactions.filter(status='PENDING').count(),
            'revenue': revenue,
            'failed': transactions.filter(status='FAILED').count()
        },
        'graph_labels_json': json.dumps(graph_labels),
        'graph_data_json': json.dumps(graph_data),
    }
    return render(request, 'merchant/dashboard.html', context)


# --- 5. PROFIL ---
@login_required(login_url='merchant_login')
def profile_view(request):
    try:
        merchant = MerchantProfile.objects.get(user=request.user)
    except MerchantProfile.DoesNotExist:
        logout(request)
        return redirect('merchant_login')

    if request.method == 'POST':
        # Mise à jour infos
        if 'company_name' in request.POST:
            merchant.company_name = request.POST.get('company_name')
            merchant.phone = request.POST.get('phone')
            merchant.address = request.POST.get('address')
            merchant.save()
            messages.success(request, "Informations mises à jour.")
        
        # Mise à jour paiements
        elif 'payment_type' in request.POST:
            ptype = request.POST.get('payment_type')
            if ptype == 'natcash':
                merchant.natcash_name = request.POST.get('natcash_name')
                merchant.natcash_number = request.POST.get('natcash_number')
                merchant.accepts_natcash = True
            elif ptype == 'moncash':
                merchant.moncash_name = request.POST.get('moncash_name')
                merchant.moncash_number = request.POST.get('moncash_number')
                merchant.accepts_moncash = True
            merchant.save()
            messages.success(request, "Méthode de paiement mise à jour.")

        # Changement mot de passe
        elif 'old_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Mot de passe modifié.")
            else:
                messages.error(request, "Erreur mot de passe.")

    return render(request, 'merchant/profile.html', {
        'merchant': merchant,
        'nom_entreprise': merchant.company_name
    })


# --- 6. API ---
@login_required(login_url='merchant_login')
def api_view(request):
    try:
        merchant = MerchantProfile.objects.get(user=request.user)
    except MerchantProfile.DoesNotExist:
        logout(request)
        return redirect('merchant_login')

    return render(request, 'merchant/api.html', {
        'merchant': merchant,
        'nom_entreprise': merchant.company_name
    })


# --- 7. SUPPRESSION ---
@login_required(login_url='merchant_login')
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Compte supprimé.")
        return redirect('merchant_login')
    return redirect('merchant_profile')

@login_required(login_url='merchant_login')
def export_transactions_csv(request):
    merchant = MerchantProfile.objects.get(user=request.user)
    transactions = Transaction.objects.filter(merchant=merchant).order_by('-created_at')

    # Création de la réponse HTTP avec le type CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="transactions_{merchant.company_name}.csv"'

    writer = csv.writer(response)
    # L'en-tête des colonnes
    writer.writerow(['Reference', 'Date', 'Client', 'Methode', 'Montant', 'Statut'])

    # Les données
    for t in transactions:
        writer.writerow([
            t.reference_id,
            t.created_at.strftime("%d/%m/%Y %H:%M"),
            t.payer_name or "Anonyme",
            t.provider or "-",
            t.amount,
            t.status
        ])

    return response

# This section continues from above - merchant_api view

# Dans merchant/views.py

# --- 6. API ---
@login_required(login_url='merchant_login')
def merchant_api(request):
    try:
        # CORRECTION : On utilise MerchantProfile (comme dans le reste de ton code)
        merchant = MerchantProfile.objects.get(user=request.user)
    except MerchantProfile.DoesNotExist:
        return redirect('merchant_dashboard')

    # --- GÉNÉRATION DU CODE STARTER KIT ---
    
    # 1. On prépare les données à injecter (Clé API + Nom)
    context_demo = {
        'api_key': merchant.api_key,
        'nom_boutique': "Boutique " + merchant.company_name
    }

    # 2. On lit le fichier 'boutique_demo.html' et on le transforme en texte
    try:
        # On utilise le vrai nom de fichier que tu as créé : 'boutique_demo.html'
        code_source = render_to_string('merchant/boutique_demo.html', context_demo)
    except Exception as e:
        # En cas d'erreur, on l'affiche dans la boîte noire pour comprendre
        code_source = f"Erreur technique : Le fichier 'merchant/templates/merchant/boutique_demo.html' est introuvable ou illisible.\nDétail : {e}"

    # --------------------------------------

    context = {
        'merchant': merchant,
        'nom_entreprise': merchant.company_name,
        'demo_code': code_source # La variable qui remplit la boîte noire
    }
    
    return render(request, 'merchant/api.html', context)


# --- VUE POUR LA DÉMO LIVE (Bouton Vert) ---
@login_required(login_url='merchant_login')
def demo_boutique(request):
    """
    Page de démonstration live qui simule un site marchand utilisant l'API
    """
    try:
        merchant = MerchantProfile.objects.get(user=request.user)
    except MerchantProfile.DoesNotExist:
        return redirect('merchant_login')
    
    context = {
        'api_key': merchant.api_key,
        'nom_boutique': "Boutique Démo - " + merchant.company_name
    }
    # On pointe bien vers le fichier qui existe
    return render(request, 'merchant/boutique_demo.html', context)





