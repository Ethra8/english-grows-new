(() => {
    const form = document.querySelector('[data-placement-form]');
    if (!form) return;

    const intro = form.querySelector('[data-intro]');
    const assessment = form.querySelector('[data-assessment]');
    const start = form.querySelector('[data-start]');
    const startError = form.querySelector('[data-start-error]');
    const focusTarget = form.querySelector('[data-assessment-focus]');
    const email = form.querySelector('[name="email"]');
    const acknowledge = form.querySelector('[name="acknowledge"]');

    const pages = [...form.querySelectorAll('[data-page]')];
    const prev = form.querySelector('[data-prev]');
    const next = form.querySelector('[data-next]');
    const submit = form.querySelector('[data-submit]');
    const label = form.querySelector('[data-progress-label]');
    const count = form.querySelector('[data-answer-count]');
    const fill = form.querySelector('[data-progress-fill]');
    const progress = form.querySelector('.placement-progress');
    const total = form.querySelectorAll('[data-question]').length;
    const submitLabel = submit.textContent;

    const security = form.querySelector('[data-turnstile-wrap]');
    const widget = form.querySelector('[data-turnstile]');
    const response = form.querySelector('[data-turnstile-response]');
    const securityError = form.querySelector('[data-turnstile-error]');

    if (!intro || !assessment || !start || !email || !acknowledge || !pages.length ||
        !security || !widget || !response || !securityError) return;

    let current = 0;
    let started = false;
    let widgetId = null;
    let verifying = false;
    let submitting = false;

    const lastPage = pages.length - 1;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function moveToAssessment() {
        focusTarget.focus({ preventScroll: true });
        assessment.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    }

    function resetSubmission(showError = false) {
        verifying = false;
        submitting = false;
        response.value = '';
        submit.disabled = false;
        submit.textContent = submitLabel;
        securityError.hidden = !showError;
    }

    function showPage(index, moveFocus = false) {
        current = Math.max(0, Math.min(index, lastPage));

        pages.forEach((page, i) => { page.hidden = i !== current; });
        prev.hidden = current === 0;
        next.hidden = current === lastPage;
        submit.hidden = current !== lastPage;
        security.hidden = current !== lastPage;

        if (current !== lastPage && verifying) resetSubmission();

        label.textContent = `${progress.dataset.pageWord} ${current * 10 + 1}-${Math.min((current + 1) * 10, total)} ${progress.dataset.ofWord} ${total}`;

        if (moveFocus) moveToAssessment();
    }

    function updateProgress() {
        const answered = form.querySelectorAll('[data-question] input[type="radio"]:checked').length;
        count.textContent = `${answered}/${total} ${progress.dataset.answeredWord}`;
        fill.style.width = `${answered / total * 100}%`;
    }

    function validateIntro() {
        if (!email.checkValidity() || !acknowledge.checked) {
            startError.hidden = false;

            if (!email.checkValidity()) {
                email.focus();
                email.reportValidity();
            } else {
                acknowledge.focus();
                acknowledge.reportValidity();
            }

            return false;
        }

        startError.hidden = true;
        return true;
    }

    function beginTest(index = 0) {
        if (!validateIntro()) return;

        started = true;
        intro.hidden = true;
        assessment.hidden = false;
        showPage(index, true);
        updateProgress();
    }

    function returnToIntro() {
        started = false;
        intro.hidden = false;
        assessment.hidden = true;
        start.hidden = false;
        startError.hidden = false;

        intro.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    }

    function verifyAndSubmit() {
        if (!window.turnstile) {
            resetSubmission(true);
            return;
        }

        verifying = true;
        response.value = '';
        securityError.hidden = true;
        submit.disabled = true;
        submit.textContent = progress.dataset.submittingWord;

        try {
            if (widgetId === null) {
                widgetId = window.turnstile.render('#placement-turnstile', {
                    sitekey: widget.dataset.sitekey,
                    action: 'placement',
                    execution: 'execute',
                    appearance: 'execute',
                    'response-field': false,
                    retry: 'never',

                    callback: token => {
                        if (!verifying || current !== lastPage) return;

                        if (!token) {
                            resetSubmission(true);
                            return;
                        }

                        response.value = token;
                        verifying = false;
                        submitting = true;
                        form.submit();
                    },

                    'error-callback': errorCode => {
                        console.warn('Turnstile verification error:', errorCode);
                        if (!submitting) resetSubmission(true);
                        return true;
                    },

                    'expired-callback': () => {
                        if (!submitting) resetSubmission(true);
                    },

                    'timeout-callback': () => {
                        if (!submitting) resetSubmission(true);
                    },
                });

            } else {
                window.turnstile.reset(widgetId);
            }

            window.turnstile.execute(widgetId);

        } catch (error) {
            console.error('Turnstile initialization failed:', error);
            resetSubmission(true);
        }
    }

    start.addEventListener('click', () => beginTest());

    prev.addEventListener('click', () => showPage(current - 1, true));
    next.addEventListener('click', () => showPage(current + 1, true));

    form.addEventListener('change', updateProgress);

    form.addEventListener('submit', event => {
        event.preventDefault();

        if (verifying || submitting) return;

        if (!started) {
            beginTest();
            return;
        }

        if (!email.checkValidity() || !acknowledge.checked) {
            returnToIntro();
            validateIntro();
            return;
        }

        if (current !== lastPage) {
            showPage(current + 1, true);
            return;
        }

        verifyAndSubmit();
    });

    window.addEventListener('pageshow', event => {
        if (event.persisted) {
            resetSubmission();
            if (widgetId !== null && window.turnstile) window.turnstile.reset(widgetId);
        }

        updateProgress();
    });

    const invalidPage = pages.findIndex(page => page.querySelector('.errorlist'));
    const introHasErrors = Boolean(intro.querySelector('.errorlist'));
    const formHasErrors = Boolean(form.querySelector('[data-form-errors]'));
    const turnstileFailed = form.dataset.turnstileFailed === 'true';

    showPage(invalidPage >= 0 ? invalidPage : 0);
    updateProgress();
    start.hidden = false;

    if (turnstileFailed && !introHasErrors) {
        beginTest(lastPage);
        securityError.hidden = false;
    } else if (invalidPage >= 0 && !introHasErrors && !formHasErrors) {
        beginTest(invalidPage);
    } else {
        assessment.hidden = true;
    }
})();