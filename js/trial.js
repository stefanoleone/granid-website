// Granid — trial form submit handler (GWEB-10)
// Posts to the CRM /leads endpoint per ECOSYSTEM.md "Trial request form".
// Awaiting CRM endpoint to be live + CORS for granid.ch / www.granid.ch.

(function () {
  'use strict';

  var CRM_ENDPOINT = 'https://crm.granid.ch/api/v1/leads';

  // Soft client-side blocklist for personal email domains. The CRM is the
  // authoritative gate (see ECOSYSTEM.md error code `personal_email_domain`);
  // this list exists only to fail fast in the browser before the round-trip.
  var PERSONAL_DOMAINS = [
    'gmail.com', 'googlemail.com',
    'hotmail.com', 'hotmail.ch', 'hotmail.fr', 'hotmail.de', 'hotmail.it',
    'outlook.com', 'outlook.ch', 'outlook.fr', 'outlook.de', 'outlook.it',
    'live.com', 'live.ch', 'live.fr', 'msn.com',
    'yahoo.com', 'yahoo.fr', 'yahoo.de', 'yahoo.it', 'ymail.com',
    'icloud.com', 'me.com', 'mac.com',
    'proton.me', 'protonmail.com', 'protonmail.ch', 'pm.me',
    'gmx.ch', 'gmx.com', 'gmx.de', 'gmx.net',
    'bluewin.ch', 'sunrise.ch', 'hispeed.ch', 'swissonline.ch'
  ];

  // Localized copy for every error code the CRM may return + the redirect
  // path on success.
  var I18N = {
    en: {
      personal_email_domain: 'Please use a company email address. Personal email providers like gmail.com or hotmail.com are not eligible for the trial.',
      already_trialed: 'Your firm has already redeemed a trial. Visit our contact page to discuss a paid license.',
      website_invalid: 'Please enter a valid website (for example, example.ch).',
      privacy_not_acknowledged: 'You must acknowledge the data-privacy notice to continue.',
      generic: 'Something went wrong. Please try again or visit our contact page.',
      submitting: 'Sending…',
      trialSentPath: '/trial-sent/'
    },
    de: {
      personal_email_domain: 'Bitte verwenden Sie eine geschäftliche E-Mail-Adresse. Persönliche E-Mail-Anbieter wie gmail.com oder hotmail.com sind für den Trial nicht zulässig.',
      already_trialed: 'Ihre Kanzlei hat den Trial bereits eingelöst. Besuchen Sie unsere Kontaktseite für eine bezahlte Lizenz.',
      website_invalid: 'Bitte geben Sie eine gültige Website ein (z. B. example.ch).',
      privacy_not_acknowledged: 'Sie müssen den Datenschutzhinweis bestätigen, um fortzufahren.',
      generic: 'Etwas ist schiefgelaufen. Bitte versuchen Sie es erneut oder besuchen Sie unsere Kontaktseite.',
      submitting: 'Wird gesendet…',
      trialSentPath: '/de/trial-sent/'
    },
    fr: {
      personal_email_domain: 'Veuillez utiliser une adresse e-mail professionnelle. Les fournisseurs personnels comme gmail.com ou hotmail.com ne sont pas éligibles pour l’essai.',
      already_trialed: 'Votre étude a déjà bénéficié de l’essai. Consultez notre page de contact pour discuter d’une licence payante.',
      website_invalid: 'Veuillez saisir un site web valide (par exemple, example.ch).',
      privacy_not_acknowledged: 'Vous devez accepter la notice de confidentialité pour continuer.',
      generic: 'Une erreur est survenue. Veuillez réessayer ou consulter notre page de contact.',
      submitting: 'Envoi…',
      trialSentPath: '/fr/trial-sent/'
    },
    it: {
      personal_email_domain: 'Usi un indirizzo email aziendale. I provider personali come gmail.com o hotmail.com non sono ammessi per la prova.',
      already_trialed: 'Il Suo studio ha già usato la prova. Visiti la pagina dei contatti per una licenza a pagamento.',
      website_invalid: 'Inserisca un sito web valido (per esempio, example.ch).',
      privacy_not_acknowledged: 'Deve accettare l’informativa sulla privacy per continuare.',
      generic: 'Qualcosa è andato storto. Riprovi o visiti la pagina dei contatti.',
      submitting: 'Invio in corso…',
      trialSentPath: '/it/trial-sent/'
    }
  };

  // Stable error codes that map to a specific field; everything else
  // surfaces in the global error box.
  var ERROR_CODE_FIELD = {
    personal_email_domain: 'email',
    website_invalid: 'website',
    privacy_not_acknowledged: 'data_privacy_acknowledged'
  };

  var form = document.getElementById('trial-form');
  if (!form) return;

  var localeInput = form.querySelector('input[name="locale"]');
  var locale = (localeInput && localeInput.value) || 'en';
  var messages = I18N[locale] || I18N.en;
  var globalErrorEl = document.getElementById('trial-error-global');

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
    if (!errorEl) {
      showGlobalError(msg);
      return;
    }
    errorEl.textContent = msg;
    errorEl.classList.add('active');
    var input = form.querySelector('[name="' + fieldName + '"]');
    if (input) input.setAttribute('aria-invalid', 'true');
  }

  function showGlobalError(msg) {
    if (!globalErrorEl) return;
    globalErrorEl.textContent = msg;
    globalErrorEl.classList.add('active');
  }

  function isPersonalEmail(email) {
    var at = email.lastIndexOf('@');
    if (at < 0) return false;
    return PERSONAL_DOMAINS.indexOf(email.slice(at + 1).toLowerCase()) >= 0;
  }

  function gatherFormData() {
    var fd = new FormData(form);
    return {
      first_name: (fd.get('first_name') || '').trim(),
      last_name: (fd.get('last_name') || '').trim(),
      email: (fd.get('email') || '').trim(),
      website: normalizeUrl((fd.get('website') || '').trim()),
      firm_address: (fd.get('firm_address') || '').trim(),
      company_size: fd.get('company_size') || '',
      has_it_support: fd.get('has_it_support') === 'true',
      data_privacy_acknowledged: form.querySelector('input[name="data_privacy_acknowledged"]').checked,
      locale: fd.get('locale') || 'en'
    };
  }

  function normalizeUrl(value) {
    if (!value) return value;
    // Strip any existing scheme so we always end up with https://
    var stripped = value.replace(/^[a-z][a-z0-9+.-]*:\/*/i, '');
    return 'https://' + stripped;
  }

  function clientValidate(data) {
    var firstError = null;
    if (data.website && !/^https:\/\/[^\s.]+\.[^\s]+$/i.test(data.website)) {
      showFieldError('website', messages.website_invalid);
      firstError = firstError || 'website';
    }
    if (data.email && isPersonalEmail(data.email)) {
      showFieldError('email', messages.personal_email_domain);
      firstError = firstError || 'email';
    }
    if (!data.data_privacy_acknowledged) {
      showFieldError('data_privacy_acknowledged', messages.privacy_not_acknowledged);
      firstError = firstError || 'data_privacy_acknowledged';
    }
    return firstError;
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
        window.location.href = messages.trialSentPath;
        return;
      }
      return res.json().then(function (body) {
        return body && body.error;
      }, function () { return null; }).then(function (errorCode) {
        if (errorCode && messages[errorCode]) {
          var field = ERROR_CODE_FIELD[errorCode];
          if (field) showFieldError(field, messages[errorCode]);
          else showGlobalError(messages[errorCode]);
        } else {
          showGlobalError(messages.generic);
        }
        btn.disabled = false;
        btn.textContent = originalText;
      });
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
    if (clientValidate(data)) return;

    submit(data, form.querySelector('button[type="submit"]'));
  });
})();
