// Granid — enterprise inquiry submit handler (GWEB-15)
// Posts to the CRM endpoint that handles the Enterprise sales pipeline.
//
// Endpoint path is provisional: per LEGALINT-171, the CRM team needs to
// confirm whether enterprise inquiries get their own endpoint
// (POST /api/v1/leads/enterprise) or share /api/v1/leads with a
// `tier_interest: "enterprise"` discriminator. We are using the dedicated
// path here. If the CRM team picks the shared-endpoint option, swap the
// URL constant and add the discriminator to the body.

(function () {
  'use strict';

  var CRM_ENDPOINT = 'https://crm.granid.ch/api/v1/leads/enterprise';

  var SUCCESS_PATHS = {
    en: '/contact-sent/',
    de: '/de/contact-sent/',
    fr: '/fr/contact-sent/',
    it: '/it/contact-sent/'
  };

  var I18N = {
    en: {
      website_invalid: 'Please enter a valid HTTPS URL (for example, https://example.ch).',
      generic: 'Something went wrong. Please try again or email stefano@granid.ch.',
      submitting: 'Sending…'
    },
    de: {
      website_invalid: 'Bitte geben Sie eine gültige HTTPS-URL ein (z. B. https://example.ch).',
      generic: 'Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut oder schreiben Sie an stefano@granid.ch.',
      submitting: 'Wird gesendet…'
    },
    fr: {
      website_invalid: 'Veuillez saisir une URL HTTPS valide (par exemple, https://example.ch).',
      generic: 'Une erreur est survenue. Veuillez réessayer ou écrire à stefano@granid.ch.',
      submitting: 'Envoi…'
    },
    it: {
      website_invalid: 'Inserisca un URL HTTPS valido (per esempio https://example.ch).',
      generic: 'Qualcosa è andato storto. Riprovi o scriva a stefano@granid.ch.',
      submitting: 'Invio in corso…'
    }
  };

  var form = document.getElementById('enterprise-form');
  if (!form) return;

  var localeInput = form.querySelector('input[name="locale"]');
  var locale = (localeInput && localeInput.value) || 'en';
  var messages = I18N[locale] || I18N.en;
  var globalErrorEl = document.getElementById('enterprise-error-global');

  function clearErrors() {
    if (globalErrorEl) {
      globalErrorEl.classList.remove('active');
      globalErrorEl.textContent = '';
    }
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

  function showGlobalError(msg) {
    if (!globalErrorEl) return;
    globalErrorEl.textContent = msg;
    globalErrorEl.classList.add('active');
  }

  function gatherFormData() {
    var fd = new FormData(form);
    var seats = parseInt(fd.get('estimated_seats') || '0', 10);
    return {
      first_name: (fd.get('first_name') || '').trim(),
      last_name: (fd.get('last_name') || '').trim(),
      email: (fd.get('email') || '').trim(),
      firm_name: (fd.get('firm_name') || '').trim(),
      firm_address: (fd.get('firm_address') || '').trim(),
      firm_website: (fd.get('firm_website') || '').trim(),
      company_size: fd.get('company_size') || '',
      estimated_seats: isNaN(seats) ? 0 : seats,
      message: (fd.get('message') || '').trim(),
      locale: fd.get('locale') || 'en'
    };
  }

  function submit(data, btn) {
    btn.disabled = true;
    var originalText = btn.textContent;
    btn.textContent = messages.submitting;

    fetch(CRM_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (res) {
      if (res.ok) {
        window.location.href = SUCCESS_PATHS[locale] || SUCCESS_PATHS.en;
        return;
      }
      showGlobalError(messages.generic);
      btn.disabled = false;
      btn.textContent = originalText;
    }).catch(function () {
      showGlobalError(messages.generic);
      btn.disabled = false;
      btn.textContent = originalText;
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearErrors();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var data = gatherFormData();

    if (data.firm_website && !/^https:\/\//i.test(data.firm_website)) {
      showFieldError('firm_website', messages.website_invalid);
      return;
    }

    submit(data, form.querySelector('button[type="submit"]'));
  });
})();
