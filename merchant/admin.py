# merchant/admin.py

from django.contrib import admin
from .models import MerchantProfile


# Enregistrer MerchantProfile
@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    # Les champs doivent correspondre à ceux définis dans MerchantProfile
    list_display = ("company_name", "user_email", "phone") 
    search_fields = ("company_name", "user__email")

    # Fonction pour afficher l'email de l'utilisateur (utile car l'email est dans le modèle User)
    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email