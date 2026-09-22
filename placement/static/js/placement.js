(() => {
    const form = document.querySelector('[data-placement-form]');
    if (!form) return;
    const pages = [...form.querySelectorAll('[data-page]')];
    const prev = form.querySelector('[data-prev]');
    const next = form.querySelector('[data-next]');
    const submit = form.querySelector('[data-submit]');
    const label = form.querySelector('[data-progress-label]');
    const count = form.querySelector('[data-answer-count]');
    const fill = form.querySelector('[data-progress-fill]');
    const progress = form.querySelector('.placement-progress');
    const total = form.querySelectorAll('[data-question]').length;
    let current = 0;

    function showPage(index) {
        current = Math.max(0, Math.min(index, pages.length - 1));
        pages.forEach((page, i) => { page.hidden = i !== current; });
        prev.hidden = current === 0;
        next.hidden = current === pages.length - 1;
        submit.hidden = current !== pages.length - 1;
        label.textContent = `${progress.dataset.pageWord} ${current * 10 + 1}-${Math.min((current + 1) * 10, total)} ${progress.dataset.ofWord} ${total}`;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateProgress() {
        const answered = form.querySelectorAll('[data-question] input[type="radio"]:checked').length;
        count.textContent = `${answered}/${total} ${progress.dataset.answeredWord}`;
        fill.style.width = `${answered / total * 100}%`;
    }

    prev.addEventListener('click', () => showPage(current - 1));
    next.addEventListener('click', () => showPage(current + 1));
    form.addEventListener('change', updateProgress);
    form.addEventListener('submit', () => { submit.disabled = true; submit.textContent = progress.dataset.submittingWord; });
    const invalidPage = pages.findIndex(page => page.querySelector('.errorlist'));
    showPage(invalidPage >= 0 ? invalidPage : 0);
    updateProgress();
})();
