from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from merchant.models import MerchantProfile
from .models import Transaction
import json

class FullPaymentCycleTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. On crée d'abord un Utilisateur Django (Obligatoire)
        self.user = User.objects.create_user(username='test_merchant', password='password123')

        # 2. On crée le profil marchand lié à cet utilisateur
        # J'ai retiré 'email=' car ton modèle ne l'a pas
        self.merchant = MerchantProfile.objects.create(
            user=self.user, 
            company_name="Test Corp",
            api_key="sk_test_12345"
        )
        
        # L'URL de l'API (assure-toi que le 'name' est bon dans urls.py)
        self.initiate_url = reverse('api_initiate_payment')

    def test_api_generation_url(self):
        """Vérifie que l'API renvoie bien une URL de paiement"""
        payload = {
            "api_key": "sk_test_12345",
            "amount": 1000.00,
            "description": "Test Unitaire"
        }
        
        response = self.client.post(
            self.initiate_url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('http', data['payment_url']) 

    def test_simulation_frontend_ajax(self):
        """Vérifie que la simulation renvoie bien du JSON pour le JavaScript"""
        # On crée une transaction
        tx = Transaction.objects.create(merchant=self.merchant, amount=500)
        
        # On récupère l'URL de simulation
        url = reverse('simulate_provider', args=[tx.reference_id, 'moncash'])
        
        # On simule l'appel AJAX
        response = self.client.post(url, content_type='application/json')
        
        # Vérifications
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        
        tx.refresh_from_db()
        self.assertEqual(tx.status, 'success')

    def test_security_invalid_key(self):
        """Test: Une mauvaise clé API doit être rejetée"""
        payload = {"api_key": "FAUSSE_CLE", "amount": 100}
        response = self.client.post(
            self.initiate_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)