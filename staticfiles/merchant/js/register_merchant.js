// register_merchant.js
'use strict';

// ----------------------------------------------------
// 1. DÉFINITION DES FONCTIONS UTILITAIRES (Hors DOMContentLoaded)
// Ces fonctions ne dépendent pas des éléments HTML spécifiques.
// ----------------------------------------------------

// Animation smooth pour l'affichage des formulaires
function smoothToggle(element, show) {
    if (!element) return; // Sécurité au cas où l'élément est null
    
    if (show) {
        element.style.display = 'block';
        element.style.opacity = '0';
        element.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.3s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 10);
    } else {
        element.style.transition = 'all 0.3s ease';
        element.style.opacity = '0';
        element.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            element.style.display = 'none';
        }, 300);
    }
}

// Fonction pour définir les champs requis
function setRequiredFields(paymentType, isRequired) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    fields.forEach(field => {
        field.required = isRequired;
        if (!isRequired) {
            field.classList.remove('is-invalid', 'is-valid');
        }
    });
}

// Fonction pour vider les champs d'un formulaire
function clearFormFields(paymentType) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    fields.forEach(field => {
        field.value = '';
        field.classList.remove('is-invalid', 'is-valid');
    });
}

// Fonction de validation des champs de paiement
function validatePaymentForm(paymentType) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    let isValid = true;
    
    fields.forEach(field => {
        // Validation simple: si requis et vide
        if (field.required && !field.value.trim()) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
            if (field.value.trim()) {
                field.classList.add('is-valid');
            } else {
                field.classList.remove('is-valid');
            }
        }
    });
    
    return isValid;
}


// ----------------------------------------------------
// 2. LOGIQUE PRINCIPALE (Doit être dans DOMContentLoaded)
// ----------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    let attemptedSubmit = false;
    console.log('register_merchant.js chargé (staticfiles)');

    // Fonction pour afficher/masquer les formulaires de paiement
    function togglePaymentForms() {
        // IMPORTANT : Ces éléments sont maintenant récupérés à l'intérieur de la fonction
        // ou au moins à l'intérieur de DOMContentLoaded.
        const natcashChecked = document.getElementById('natcash').checked;
        const moncashChecked = document.getElementById('moncash').checked;
        const natcashForm = document.getElementById('natcash-form');
        const moncashForm = document.getElementById('moncash-form');
        const paymentError = document.getElementById('payment-error');
        const submitBtn = document.getElementById('submit-btn');

        // Afficher/masquer les formulaires selon les checkboxes
        if (natcashChecked) {
            smoothToggle(natcashForm, true);
            setRequiredFields('natcash', true);
        } else {
            smoothToggle(natcashForm, false);
            setRequiredFields('natcash', false);
            clearFormFields('natcash');
        }

        if (moncashChecked) {
            smoothToggle(moncashForm, true);
            setRequiredFields('moncash', true);
        } else {
            smoothToggle(moncashForm, false);
            setRequiredFields('moncash', false);
            clearFormFields('moncash');
        }

        // Validation : au moins une checkbox doit être cochée
        if (!natcashChecked && !moncashChecked) {
            if (paymentError) {
                paymentError.classList.toggle('d-none', !attemptedSubmit);
            }
            // Ne pas désactiver le bouton : on permet au submit d'être cliqué et on gère la validation à la soumission
        } else {
            if (paymentError) paymentError.style.display = 'none'; // Cache l'erreur
        }
    }


    // 3. LOGIQUE D'INITIALISATION ET ÉCOUTEURS D'ÉVÉNEMENTS

    // Appel initial pour définir l'état du formulaire au chargement de la page
    // (Très important pour gérer l'état initial des checkboxes/boutons)
    togglePaymentForms();

    // Écouteurs d'événements pour les checkboxes (natcash et moncash)
    const natcashCheckbox = document.getElementById('natcash');
    const moncashCheckbox = document.getElementById('moncash');
    
    if (natcashCheckbox) {
        natcashCheckbox.addEventListener('change', togglePaymentForms);
    }
    if (moncashCheckbox) {
        moncashCheckbox.addEventListener('change', togglePaymentForms);
    }
    
    // --- Validation en temps réel ---
    const paymentFields = document.querySelectorAll('[name^="natcash_"], [name^="moncash_"]');
    paymentFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.required) {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            }
        });
        
        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });


    // --- Validation du Formulaire (Soumission) ---
    const forms = document.querySelectorAll('.needs-validation')
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            const natcashChecked = document.getElementById('natcash').checked;
            const moncashChecked = document.getElementById('moncash').checked;
            const paymentError = document.getElementById('payment-error');
            
            // Vérifier qu'au moins un moyen de paiement est sélectionné
            if (!natcashChecked && !moncashChecked) {
                event.preventDefault();
                event.stopPropagation();
                attemptedSubmit = true;
                if (paymentError) {
                    paymentError.classList.remove('d-none');
                    console.log('Afficher le message d\'erreur de paiement après soumission (register_merchant.js - staticfiles)');
                }
                return false;
            } else {
                if (paymentError) paymentError.classList.add('d-none');
            }
            
            // Validation des champs requis pour chaque méthode sélectionnée
            let paymentFormsValid = true;
            
            if (natcashChecked) {
                paymentFormsValid = validatePaymentForm('natcash');
            }
            
            if (moncashChecked) {
                // Utilisez un opérateur logique ET (&) si vous voulez que les deux validations soient testées
                // J'ai mis un opérateur ET logique ici.
                paymentFormsValid = paymentFormsValid && validatePaymentForm('moncash');
            }
            
            // Validation Bootstrap standard
            if (!form.checkValidity() || !paymentFormsValid) {
                event.preventDefault()
                event.stopPropagation()
            } else {
                console.log('Formulaire valide et prêt à être soumis!');
                
                // Le reste de ta logique de soumission/AJAX va ici
            }
            
            form.classList.add('was-validated')
        }, false)
    });

    // Définit un gestionnaire de click sur le bouton soumettre pour le cas où la validation
    // par défaut n'est pas déclenchée pour une raison quelconque (ex: conflit ou script non chargé).
    const submitBtn2 = document.getElementById('submit-btn');
    if (submitBtn2) {
        submitBtn2.addEventListener('click', function (e) {
            const nat = document.getElementById('natcash')?.checked;
            const mon = document.getElementById('moncash')?.checked;
            const paymentErrorEl = document.getElementById('payment-error');
            if (!nat && !mon) {
                // Bloquer l'action si aucun moyen de paiement sélectionné
                e.preventDefault();
                e.stopPropagation();
                attemptedSubmit = true;
                if (paymentErrorEl) paymentErrorEl.classList.remove('d-none');
                console.log('Soumission bloquée - aucun moyen de paiement sélectionné (staticfiles)');
            } else {
                console.log('Soumission : moyen de paiement sélectionné (staticfiles)');
            }
        }, { passive: false });
    }
}); // FIN de DOMContentLoaded