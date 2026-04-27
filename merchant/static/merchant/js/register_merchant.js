// register_merchant.js
'use strict';

/*----------------------------------------------------
 1. DÉFINITION DES FONCTIONS UTILITAIRES 
 ----------------------------------------------------*/

function smoothToggle(element, show) {
    if (!element) return;
    
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

function setRequiredFields(paymentType, isRequired) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    fields.forEach(field => {
        field.required = isRequired;
        if (!isRequired) {
            field.classList.remove('is-invalid', 'is-valid');
        }
    });
}

function clearFormFields(paymentType) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    fields.forEach(field => {
        field.value = '';
        field.classList.remove('is-invalid', 'is-valid');
    });
}

function validatePaymentForm(paymentType) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    let isValid = true;
    
    fields.forEach(field => {
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
// 2. LOGIQUE PRINCIPALE (Dans DOMContentLoaded)
// ----------------------------------------------------

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    function togglePaymentForms() {
        const natcashChecked = document.getElementById('natcash')?.checked || false;
        const moncashChecked = document.getElementById('moncash')?.checked || false;
        
        const natcashForm = document.getElementById('natcash-form');
        const moncashForm = document.getElementById('moncash-form');
        const paymentError = document.getElementById('payment-error');
        
        // Afficher/masquer les formulaires selon les checkboxes
        if (natcashForm) {
            if (natcashChecked) {
                smoothToggle(natcashForm, true);
                setRequiredFields('natcash', true);
            } else {
                smoothToggle(natcashForm, false);
                setRequiredFields('natcash', false);
                clearFormFields('natcash');
            }
        }

        if (moncashForm) {
            if (moncashChecked) {
                smoothToggle(moncashForm, true);
                setRequiredFields('moncash', true);
            } else {
                smoothToggle(moncashForm, false);
                setRequiredFields('moncash', false);
                clearFormFields('moncash');
            }
        }

        // Validation du bouton et affichage/masquage de l'erreur en temps réel
        if (paymentError) {
            if (!natcashChecked && !moncashChecked) {
                paymentError.style.display = 'block'; 
            } else {
                paymentError.style.display = 'none'; 
            }
        }
    }


    // 3. LOGIQUE D'INITIALISATION ET ÉCOUTEURS D'ÉVÉNEMENTS
    togglePaymentForms(); 
    
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
            if (this.required && this.closest('.payment-form')?.style.display !== 'none') {
                if (!this.value.trim()) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            } else if (!this.required) {
                this.classList.remove('is-invalid', 'is-valid');
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
            const natcashChecked = document.getElementById('natcash')?.checked;
            const moncashChecked = document.getElementById('moncash')?.checked;
            const paymentError = document.getElementById('payment-error');
            
            // Validation 1: Au moins un paiement sélectionné
            if (!natcashChecked && !moncashChecked) {
                event.preventDefault();
                event.stopPropagation();
                
                if (paymentError) {
                    paymentError.style.display = 'block';
                }
                form.classList.add('was-validated'); 
                
                return;
            } else {
                if (paymentError) {
                    paymentError.style.display = 'none';
                }
            }
            
            // Validation 2: Tous les champs visibles sont remplis
            let paymentFormsValid = true;
            
            if (natcashChecked) {
                paymentFormsValid &&= validatePaymentForm('natcash');
            }
            
            if (moncashChecked) {
                paymentFormsValid &&= validatePaymentForm('moncash');
            }
            
            // Validation 3: Validation Bootstrap standard et paiementFormsValid
            if (!form.checkValidity() || !paymentFormsValid) {
                event.preventDefault()
                event.stopPropagation()
            } else {
                console.log('Formulaire valide et prêt à être soumis!');
            }
            
            form.classList.add('was-validated')
        }, false)
    });
});