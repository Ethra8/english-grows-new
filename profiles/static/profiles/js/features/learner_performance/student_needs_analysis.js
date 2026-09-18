document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#needsAnalysisForm");
    const wizard = document.querySelector("#needsAnalysisWizard");

    if (!form || !wizard) return;

    const track = wizard.querySelector(".needs-analysis-wizard__track");
    const pages = [...wizard.querySelectorAll("[data-step-panel]")];
    const tabs = [...document.querySelectorAll(".needs-analysis-progress__item")];
    const nextButtons = [...wizard.querySelectorAll(".needs-analysis-next")];
    const backButtons = [...wizard.querySelectorAll(".needs-analysis-back")];

    const accentOtherCheckbox = form.querySelector(
        'input[name="accent_exposure"][value="other"]'
    );
    const accentOtherField = form.querySelector(".needs-analysis-accent-other");
    const accentOtherInput = form.querySelector('[name="accent_exposure_other"]');

    let currentStep = 0;
    let maxStepReached = 0;


    function updateWizardHeight() {
        const page = pages[currentStep];
        if (!page) return;

        wizard.style.height = `${page.scrollHeight}px`;
    }


    function showStep(step) {
        currentStep = Math.max(
            0,
            Math.min(step, pages.length - 1)
        );

        track.style.transform = `translateX(-${currentStep * 100}%)`;

        pages.forEach((page, index) => {
            const active = index === currentStep;

            page.setAttribute(
                "aria-hidden",
                String(!active)
            );

            page.inert = !active;
        });

        tabs.forEach((tab, index) => {
            const active = index === currentStep;

            tab.classList.toggle(
                "active",
                active
            );

            if (active) {
                tab.setAttribute(
                    "aria-current",
                    "step"
                );
            } else {
                tab.removeAttribute(
                    "aria-current"
                );
            }

            tab.disabled = index > maxStepReached;
        });

        requestAnimationFrame(
            updateWizardHeight
        );
    }


    function validateStep(step) {
        const page = pages[step];

        if (!page) return true;

        const fields = [
            ...page.querySelectorAll(
                "input, select, textarea"
            ),
        ];

        for (const field of fields) {
            if (
                field.disabled ||
                field.type === "hidden"
            ) {
                continue;
            }

            if (!field.checkValidity()) {
                field.reportValidity();
                field.focus();

                return false;
            }
        }

        if (
            accentOtherCheckbox &&
            accentOtherInput &&
            page.contains(accentOtherCheckbox) &&
            accentOtherCheckbox.checked &&
            !accentOtherInput.value.trim()
        ) {
            accentOtherInput.setCustomValidity(
                "Please specify the other accent or variety of English."
            );

            accentOtherInput.reportValidity();
            accentOtherInput.focus();

            return false;
        }

        if (accentOtherInput) {
            accentOtherInput.setCustomValidity("");
        }

        return true;
    }


    function updateAccentOtherField() {
        if (
            !accentOtherCheckbox ||
            !accentOtherField ||
            !accentOtherInput
        ) {
            return;
        }

        const show = accentOtherCheckbox.checked;

        accentOtherField.hidden = !show;

        if (!show) {
            accentOtherInput.value = "";
            accentOtherInput.setCustomValidity("");
        }

        requestAnimationFrame(
            updateWizardHeight
        );
    }


    nextButtons.forEach(button => {
        button.addEventListener("click", () => {
            if (!validateStep(currentStep)) {
                return;
            }

            maxStepReached = Math.max(
                maxStepReached,
                currentStep + 1
            );

            showStep(currentStep + 1);
        });
    });


    backButtons.forEach(button => {
        button.addEventListener("click", () => {
            showStep(currentStep - 1);
        });
    });


    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            if (index <= maxStepReached) {
                showStep(index);
            }
        });
    });


    if (accentOtherCheckbox) {
        accentOtherCheckbox.addEventListener(
            "change",
            updateAccentOtherField
        );
    }


    if (accentOtherInput) {
        accentOtherInput.addEventListener("input", () => {
            accentOtherInput.setCustomValidity("");
        });
    }


    window.addEventListener(
        "resize",
        updateWizardHeight
    );


    const firstErrorStep = pages.findIndex(page =>
        page.querySelector(
            ".needs-analysis-field--error, .needs-analysis-field__errors"
        )
    );

    if (firstErrorStep >= 0) {
        currentStep = firstErrorStep;
        maxStepReached = firstErrorStep;
    }


    updateAccentOtherField();
    showStep(currentStep);
});