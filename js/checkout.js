// Granid — fake checkout flow (GWEB-12)
// Simulates a Stripe Checkout redirect for design/UX validation.
// The form pretends to forward the user to a payment page, then lands
// them on /buy/success after a short delay so the funnel can be walked
// end-to-end before any payment integration exists.
//
// TODO: replace this stub with a POST to crm.granid.ch/api/v1/checkout/draft
// when the Stripe integration lands (see ECOSYSTEM.md update tracked in
// LEGALINT-171, "Self-service paid lifecycle"). The CRM will return
// { checkout_url } and this handler will redirect the browser there
// instead of /buy/success.

(function () {
  'use strict';

  var SUCCESS_PATHS = {
    en: '/buy/success/',
    de: '/de/buy/success/',
    fr: '/fr/buy/success/',
    it: '/it/buy/success/'
  };

  var I18N = {
    en: {
      redirecting: 'Redirecting to payment…',
      website_invalid: 'Please enter a valid HTTPS URL (for example, https://example.ch).'
    },
    de: {
      redirecting: 'Weiterleitung zur Zahlung…',
      website_invalid: 'Bitte geben Sie eine gültige HTTPS-URL ein (z. B. https://example.ch).'
    },
    fr: {
      redirecting: 'Redirection vers le paiement…',
      website_invalid: 'Veuillez saisir une URL HTTPS valide (par exemple, https://example.ch).'
    },
    it: {
      redirecting: 'Reindirizzamento al pagamento…',
      website_invalid: 'Inserisci un URL HTTPS valido (per esempio https://example.ch).'
    }
  };

  var form = document.getElementById('checkout-form');
  if (!form) return;

  var localeInput = form.querySelector('input[name="locale"]');
  var locale = (localeInput && localeInput.value) || 'en';
  var messages = I18N[locale] || I18N.en;

  function clearErrors() {
    var perField = form.querySelectorAll('.form-error');
    for (var i = 0; i < perField.length; i++) {
      perField[i].classList.remove('active');
      perField[i].textContent = '';
    }
    var invalid = form.querySelectorAll('[aria-invalid="true"]');
    for (var j = 0; j < invalid.length; j++) {
      invalid[j].removeAttribute('aria-invalid');
    }
  }

  function showFieldError(fieldName, msg) {
    var errorEl = form.querySelector('[data-error-for="' + fieldName + '"]');
    if (errorEl) {
      errorEl.textContent = msg;
      errorEl.classList.add('active');
    }
    var input = form.querySelector('[name="' + fieldName + '"]');
    if (input) input.setAttribute('aria-invalid', 'true');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearErrors();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var website = form.querySelector('[name="firm_website"]').value.trim();
    if (website && !/^https:\/\//i.test(website)) {
      showFieldError('firm_website', messages.website_invalid);
      return;
    }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = messages.redirecting;

    setTimeout(function () {
      window.location.href = SUCCESS_PATHS[locale] || SUCCESS_PATHS.en;
    }, 1500);
  });
})();
