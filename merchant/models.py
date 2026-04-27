from django.db import models
from django.contrib.auth.models import User
import uuid  # <--- INDISPENSABLE : C'est ça qui génère les clés uniques

class MerchantProfile(models.Model):
    # Lien vers l'utilisateur
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Infos Entreprise
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)

    
    # La clé API unique pour chaque marchand
    api_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4, editable=False)
    # ---------------------------------

    # Paiements choisis
    accepts_natcash = models.BooleanField(default=False)
    accepts_moncash = models.BooleanField(default=False)
    
    # Infos NatCash
    natcash_name = models.CharField(max_length=100, blank=True, null=True)
    natcash_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Infos Moncash
    moncash_name = models.CharField(max_length=100, blank=True, null=True)
    moncash_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.email})"