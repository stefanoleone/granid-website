// Granid — generic contact-us submit handler.
//
// POSTs to the shared CRM leads endpoint with `tier_interest: "contact"`
// as the discriminator, per ECOSYSTEM.md (LEGALINT-194 update). The CRM
// endpoint contract is tracked in GCRM-N (follow-up). Until the CRM is
// wired up, this form ships in "blocked-by-crm" mode: the network call
// fails and the user sees the generic error message.

(function () {
  'use strict';

  // Local CRM override: when serving from localhost during dev, point at the
  // local CRM (FastAPI on :8000) so the form is testable end-to-end.
  var CRM_ENDPOINT =
    (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
      ? 'http://127.0.0.1:8000/api/v1/leads'
      : 'https://crm.granid.ch/api/v1/leads';

  var SUCCESS_PATHS = {
    en: '/contact-sent/',
    de: '/de/contact-sent/',
    fr: '/fr/contact-sent/',
    it: '/it/contact-sent/'
  };

  var I18N = {
    en: {
      generic: 'Something went wrong. Please try again.',
      submitting: 'Sending…'
    },
    de: {
      generic: 'Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut.',
      submitting: 'Wird gesendet…'
    },
    fr: {
      generic: 'Une erreur est survenue. Veuillez réessayer.',
      submitting: 'Envoi…'
    },
    it: {
      generic: 'Qualcosa è andato storto. Riprovi.',
      submitting: 'Invio in corso…'
    }
  };

  var form = document.getElementById('contact-form');
  if (!form) return;

  var localeInput = form.querySelector('input[name="locale"]');
  var locale = (localeInput && localeInput.value) || 'en';
  var messages = I18N[locale] || I18N.en;
  var globalErrorEl = document.getElementById('contact-error-global');

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

  function showGlobalError(msg) {
    if (!globalErrorEl) return;
    globalErrorEl.textContent = msg;
    globalErrorEl.classList.add('active');
  }

  function gatherFormData() {
    var fd = new FormData(form);
    return {
      tier_interest: 'contact',
      first_name: (fd.get('first_name') || '').trim(),
      last_name: (fd.get('last_name') || '').trim(),
      email: (fd.get('email') || '').trim(),
      firm_name: (fd.get('firm_name') || '').trim(),
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

    submit(gatherFormData(), form.querySelector('button[type="submit"]'));
  });
})();
