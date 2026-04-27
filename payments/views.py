from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import Transaction
from merchant.models import MerchantProfile

# --- 1. API D'INITIALISATION ---
@csrf_exempt
def api_initiate_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            api_key = data.get('api_key')
            amount = data.get('amount')
            description = data.get('description', 'Achat')

            if not api_key or not amount:
                 return JsonResponse({'error': 'Données manquantes'}, status=400)

            try:
                merchant = MerchantProfile.objects.get(api_key=api_key)
            except MerchantProfile.DoesNotExist:
                return JsonResponse({'error': 'Clé API invalide'}, status=403)

            transaction = Transaction.objects.create(
                merchant=merchant,
                amount=amount,
                description=description,
                status='PENDING'
            )

            relative_path = reverse('checkout_view', args=[transaction.reference_id])
            full_payment_url = request.build_absolute_uri(relative_path)

            return JsonResponse({
                'success': True,
                'payment_url': full_payment_url,
                'reference_id': str(transaction.reference_id)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


# --- 2. PAGE DE CHECKOUT ---
def checkout_view(request, reference_id):
    transaction = get_object_or_404(Transaction, reference_id=reference_id)
    
    if str(transaction.status).upper() == 'SUCCESS':
        return redirect('payment_success', reference_id=transaction.reference_id)

    return render(request, 'payment/checkout.html', {
        'transaction': transaction,
        'merchant': transaction.merchant
    })


# --- 3. SIMULATEUR DE PAIEMENT (ENREGISTREMENT NOM & PROVIDER) ---
@csrf_exempt
def simulate_provider_view(request, reference_id, provider):
    transaction = get_object_or_404(Transaction, reference_id=reference_id)
    merchant = transaction.merchant # On récupère le marchand lié

    # --- SÉCURITÉ AJOUTÉE ---
    # Si on essaie Natcash mais que le marchand a dit NON
    if provider == 'natcash' and not merchant.accepts_natcash:
        return JsonResponse({'success': False, 'error': 'Ce marchand n\'accepte pas NatCash.'})
    
    # Si on essaie Moncash mais que le marchand a dit NON
    if provider == 'moncash' and not merchant.accepts_moncash:
        return JsonResponse({'success': False, 'error': 'Ce marchand n\'accepte pas MonCash.'})
    # ------------------------
    
    if request.method == 'POST':
        try:
            # Récupération des données envoyées par le modal (JS)
            data = json.loads(request.body)
            nom_client = data.get('payer_name')
            
            # Mise à jour de la transaction
            transaction.status = 'SUCCESS'     
            transaction.provider = provider    # On sauvegarde : "moncash" ou "natcash"
            transaction.payer_name = nom_client # On sauvegarde : "Jean Pierre"
            
            transaction.save()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return redirect('checkout_view', reference_id=transaction.reference_id)


# --- 4. PAGE DE SUCCÈS ---
def payment_success_view(request, reference_id):
    transaction = get_object_or_404(Transaction, reference_id=reference_id)
    return render(request, 'payment/success.html', {'transaction': transaction})

# Dans payments/views.py

@csrf_exempt
def api_check_status(request):
    """
    Permet au marchand de récupérer les infos d'une transaction
    pour générer SA PROPRE facture/reçu.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            api_key = data.get('api_key')
            reference_id = data.get('reference_id')

            # 1. Vérif Sécurité : Est-ce le bon marchand ?
            try:
                merchant = MerchantProfile.objects.get(api_key=api_key)
                transaction = Transaction.objects.get(reference_id=reference_id, merchant=merchant)
            except (MerchantProfile.DoesNotExist, Transaction.DoesNotExist):
                return JsonResponse({'error': 'Transaction introuvable ou accès refusé'}, status=403)

            # 2. On renvoie TOUTES les infos au marchand
            return JsonResponse({
                'success': True,
                'status': transaction.status,          # SUCCESS, PENDING...
                'amount': transaction.amount,          # 1000.00
                'reference_id': str(transaction.reference_id),
                'payer_name': transaction.payer_name,  # "Jean Pierre"
                'provider': transaction.provider,      # "MonCash"
                'created_at': transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"), # Date précise
                'description': transaction.description
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)