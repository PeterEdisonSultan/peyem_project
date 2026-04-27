/* PEYEM SDK v1.0
   Ce script gère la communication entre le site du marchand et l'API Peyem.
*/

const Peyem = {
    // URL de ton API (Change ceci quand tu mettras en ligne)
    API_URL: "http://127.0.0.1:8000/payment/api/initiate/",

    /**
     * Lance le processus de paiement
     * @param {string} apiKey - La clé publique du marchand (sk_...)
     * @param {number} amount - Le montant à payer
     * @param {string} description - Description de la commande
     */
    initiate: function(apiKey, amount, description) {
        console.log("🚀 PEYEM: Initialisation du paiement...");

        // 1. Validation basique
        if (!apiKey || !amount) {
            console.error("PEYEM Erreur: Clé API ou montant manquant.");
            alert("Erreur de configuration PEYEM. Voir la console.");
            return;
        }

        // 2. Préparation des données
        const payload = {
            api_key: apiKey,
            amount: amount,
            description: description || "Achat en ligne"
        };

        // 3. Appel à l'API (AJAX)
        fetch(this.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Pas besoin de CSRF ici car c'est une API externe
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) {
                // Si le serveur renvoie une erreur (403, 500...)
                return response.json().then(err => { throw new Error(err.error || "Erreur serveur"); });
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.payment_url) {
                console.log("✅ PEYEM: Succès ! Redirection vers", data.payment_url);
                // 4. Redirection vers la page de paiement sécurisée
                window.location.href = data.payment_url;
            } else {
                throw new Error("Réponse API invalide");
            }
        })
        .catch(error => {
            console.error("❌ PEYEM Erreur:", error.message);
            alert("Impossible d'initier le paiement : " + error.message);
        });
    }
};