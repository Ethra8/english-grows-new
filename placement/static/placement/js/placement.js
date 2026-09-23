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

    if (!intro || !assessment || !start || !email || !acknowledge || !pages.length) return;

    let current = 0;
    let started = false;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function moveToAssessment() {
        focusTarget.focus({ preventScroll: true });
        assessment.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    }

    function showPage(index, moveFocus = false) {
        current = Math.max(0, Math.min(index, pages.length - 1));

        pages.forEach((page, i) => { page.hidden = i !== current; });
        prev.hidden = current === 0;
        next.hidden = current === pages.length - 1;
        submit.hidden = current !== pages.length - 1;

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

    start.addEventListener('click', () => beginTest());

    prev.addEventListener('click', () => showPage(current - 1, true));
    next.addEventListener('click', () => showPage(current + 1, true));

    form.addEventListener('change', updateProgress);

    form.addEventListener('submit', event => {
        if (!started) {
            event.preventDefault();
            beginTest();
            return;
        }

        if (!email.checkValidity() || !acknowledge.checked) {
            event.preventDefault();
            returnToIntro();
            validateIntro();
            return;
        }

        if (current !== pages.length - 1) {
            event.preventDefault();
            showPage(current + 1, true);
            return;
        }

        submit.disabled = true;
        submit.textContent = progress.dataset.submittingWord;
    });

    window.addEventListener('pageshow', () => {
        submit.disabled = false;
        submit.textContent = submitLabel;
        updateProgress();
    });

    const invalidPage = pages.findIndex(page => page.querySelector('.errorlist'));
    const introHasErrors = Boolean(intro.querySelector('.errorlist'));
    const formHasErrors = Boolean(form.querySelector('[data-form-errors]'));

    showPage(invalidPage >= 0 ? invalidPage : 0);
    updateProgress();
    start.hidden = false;

    if (invalidPage >= 0 && !introHasErrors && !formHasErrors) {
        beginTest(invalidPage);
    } else {
        assessment.hidden = true;
    }
})();