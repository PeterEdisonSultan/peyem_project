import requests
import webbrowser # Pour ouvrir l'URL automatiquement

# L'adresse de ton serveur local
API_URL = "http://127.0.0.1:8000/payment/api/initiate/"

# REMPLACE CECI PAR LA CLÉ QUE TU AS COPIÉE DANS L'ADMIN
MA_CLE_API = "54260fb5c1354152913f36a3071adb16" 

payload = {
    "api_key": MA_CLE_API,
    "amount": 5000,
    "description": "Achat Test iPhone"
}

print(f"📡 Envoi de la demande à {API_URL}...")

try:
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        payment_url = data['payment_url']
        
        print("\n✅ SUCCÈS API !")
        print(f"🆔 Transaction ID : {data['reference_id']}")
        print(f"🔗 Lien reçu : {payment_url}")
        
        print("\n🚀 Ouverture du navigateur pour payer...")
        webbrowser.open(payment_url)
    else:
        print(f"\n❌ ERREUR API ({response.status_code}) :")
        print(response.text)

except Exception as e:
    print(f"\n❌ Impossible de se connecter : {e}")