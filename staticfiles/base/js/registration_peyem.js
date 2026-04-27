// Validation Bootstrap originale
(() => {
  'use strict'
  let attemptedSubmit = false;
  
  // Fonction pour afficher/masquer les formulaires de paiement
  function togglePaymentForms() {
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
      // Ne pas désactiver le bouton ; la validation se fera à la soumission
    } else {
      if (paymentError) paymentError.style.display = 'none';
    }
  }
  
  // Fonction pour définir les champs requis
  function setRequiredFields(paymentType, isRequired) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    fields.forEach(field => {
      field.required = isRequired;
      if (!isRequired) {
        field.classList.remove('is-invalid');
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
  
  // Animation smooth pour l'affichage des formulaires
  function smoothToggle(element, show) {
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
  
  // Fonction de validation des champs de paiement
  function validatePaymentForm(paymentType) {
    const fields = document.querySelectorAll(`[name^="${paymentType}_"]`);
    let isValid = true;
    
    fields.forEach(field => {
      if (field.required && !field.value.trim()) {
        field.classList.add('is-invalid');
        isValid = false;
      } else {
        field.classList.remove('is-invalid');
        if (field.value.trim()) {
          field.classList.add('is-valid');
        }
      }
    });
    
    return isValid;
  }
  
  // Attendre que le DOM soit chargé
  document.addEventListener('DOMContentLoaded', function() {
    console.log('registration_peyem.js chargé (staticfiles)');
    const checkboxes = document.querySelectorAll('.payment-checkbox');
    
    // Écouteurs d'événements pour les checkboxes
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', togglePaymentForms);
    });
    
    // Validation en temps réel pour les champs de paiement
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
  });
  
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')
  
  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      // Validation personnalisée pour les moyens de paiement
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
          console.log('Afficher le message d\'erreur de paiement après soumission (registration_peyem.js - staticfiles)');
        }
        return false;
      } else {
        if (paymentError) paymentError.classList.add('d-none');
      }
      
      // Validation des champs requis pour chaque méthode sélectionnée
      let paymentFormsValid = true;
      
      if (natcashChecked) {
        paymentFormsValid &= validatePaymentForm('natcash');
      }
      
      if (moncashChecked) {
        paymentFormsValid &= validatePaymentForm('moncash');
      }
      
      // Validation Bootstrap standard
      if (!form.checkValidity() || !paymentFormsValid) {
        event.preventDefault()
        event.stopPropagation()
      } else {
        // Formulaire valide - ici vous pouvez ajouter votre logique de soumission
        console.log('Formulaire valide et prêt à être soumis!');
        
        // Récupérer les données du formulaire
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
          data[key] = value;
        }
        
        // Ajouter les méthodes de paiement sélectionnées
        data.selectedPaymentMethods = [];
        if (natcashChecked) data.selectedPaymentMethods.push('natcash');
        if (moncashChecked) data.selectedPaymentMethods.push('moncash');
        
        console.log('Données du formulaire:', data);
        
        // Vous pouvez maintenant envoyer les données à votre serveur
        // event.preventDefault(); // Décommentez pour empêcher la soumission réelle pendant les tests
      }
      
      form.classList.add('was-validated')
    }, false)
  })

  // Définit un gestionnaire de click sur le bouton soumettre pour le cas où la validation
  // par défaut n'est pas déclenchée pour une raison quelconque.
  const submitBtn3 = document.getElementById('submit-btn');
  if (submitBtn3) {
    submitBtn3.addEventListener('click', function (e) {
      const nat = document.getElementById('natcash')?.checked;
      const mon = document.getElementById('moncash')?.checked;
      const paymentErrorEl = document.getElementById('payment-error');
      if (!nat && !mon) {
        e.preventDefault();
        e.stopPropagation();
        attemptedSubmit = true;
        if (paymentErrorEl) paymentErrorEl.classList.remove('d-none');
        console.log('Soumission bloquée - aucun moyen de paiement sélectionné (registration_peyem)');
      } else {
        console.log('Soumission : moyen de paiement sélectionné (registration_peyem)');
      }
    }, { passive: false });
  }
})()