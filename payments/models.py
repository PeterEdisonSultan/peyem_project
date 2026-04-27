from django.db import models
from merchant.models import MerchantProfile
import uuid

class Transaction(models.Model):
    # Identifiant unique de la transaction (ex: a1b2-c3d4...)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Lien vers le marchand qui reçoit l'argent
    merchant = models.ForeignKey(MerchantProfile, on_delete=models.CASCADE, related_name='transactions')
    
    # Informations de paiement
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, default="Achat")
    
    # Statut : PENDING (En attente), SUCCESS (Succès), FAILED (Échec)
    status = models.CharField(max_length=20, default='PENDING')
    
    # --- LES NOUVEAUX CHAMPS IMPORTANTS ---
    # provider : Pour savoir si c'était MonCash ou NatCash pour CETTE transaction
    provider = models.CharField(max_length=50, blank=True, null=True) 
    
    # payer_name : Le nom que le client a entré dans le modal
    payer_name = models.CharField(max_length=100, blank=True, null=True)
    # --------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference_id} - {self.amount} HTG ({self.status})"