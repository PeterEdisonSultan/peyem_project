# merchant/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# 🚨 CORRECTION REGEX : Commence par 3 ou 4, suivi de 7 chiffres (8 chiffres au total) 🚨
# Ceci gère le format 3xxxxxxx ou 4xxxxxxx
MOBILE_PHONE_REGEX = r"^[34]\d{7}$"


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Adresse e-mail", max_length=254)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse e-mail est déjà enregistrée. Veuillez vous connecter.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return password2

class MerchantDetailsForm(forms.Form):
    company_name = forms.CharField(max_length=100, label="Nom de votre entreprise")
    phone = forms.CharField(max_length=20, label="Téléphone")
    address = forms.CharField(max_length=255, required=False, label="Adresse de votre entreprise (optionnel)")
    payment_methods = forms.MultipleChoiceField(
        choices=[('natcash', 'NatCash'), ('moncash', 'MonCash')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    natcash_name = forms.CharField(max_length=100, required=False)
    natcash_number = forms.CharField(max_length=20, required=False)
    moncash_name = forms.CharField(max_length=100, required=False)
    moncash_number = forms.CharField(max_length=20, required=False)


    # 🚨 Message simplifié : juste "Numéro invalide" 🚨
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(MOBILE_PHONE_REGEX, phone):
            raise ValidationError("Numéro invalide.")
        return phone

    def clean_natcash_number(self):
        natcash_number = self.cleaned_data.get('natcash_number')
        if natcash_number and not re.match(MOBILE_PHONE_REGEX, natcash_number):
            raise ValidationError("Numéro NatCash invalide.")
        return natcash_number

    def clean_moncash_number(self):
        moncash_number = self.cleaned_data.get('moncash_number')
        if moncash_number and not re.match(MOBILE_PHONE_REGEX, moncash_number):
            raise ValidationError("Numéro Moncash invalide.")
        return moncash_number