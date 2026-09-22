document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#needsAnalysisForm");
    const wizard = document.querySelector("#needsAnalysisWizard");

    if (!form || !wizard) return;

    const track = wizard.querySelector(".needs-analysis-wizard__track");
    const pages = [...wizard.querySelectorAll("[data-step-panel]")];
    const progress = document.querySelector(".needs-analysis-progress");
    const tabs = [...document.querySelectorAll(".needs-analysis-progress__item")];
    const nextButtons = [...wizard.querySelectorAll(".needs-analysis-next")];
    const backButtons = [...wizard.querySelectorAll(".needs-analysis-back")];

    const accentOtherCheckbox = form.querySelector('input[name="accent_exposure"][value="other"]');
    const accentOtherField = form.querySelector(".needs-analysis-accent-other");
    const accentOtherInput = form.querySelector('[name="accent_exposure_other"]');

    const requiredCheckboxGroups = ["communication_situations", "priority_areas"];

    let currentStep = 0;
    let maxStepReached = 0;

    // Manual validation prevents browser errors on inactive/inert wizard pages.
    form.noValidate = true;


    // ---------------------------------------------------------
    // WIZARD HEIGHT
    // ---------------------------------------------------------
    function updateWizardHeight() {
        const page = pages[currentStep];
        if (!page) return;

        wizard.style.height = `${page.scrollHeight}px`;
    }


    // ---------------------------------------------------------
    // ACTIVE TAB — HORIZONTAL SCROLLING
    // ---------------------------------------------------------
    function scrollActiveTabIntoView() {
        const tab = tabs[currentStep];
        if (!tab || !progress) return;

        const tabRect = tab.getBoundingClientRect();
        const navRect = progress.getBoundingClientRect();

        progress.scrollBy({
            left: tabRect.left - navRect.left - (progress.clientWidth - tabRect.width) / 2,
            behavior: "smooth",
        });
    }


    // ---------------------------------------------------------
    // SHOW STEP
    // ---------------------------------------------------------
    function showStep(step) {
        currentStep = Math.max(0, Math.min(step, pages.length - 1));

        track.style.transform = `translateX(-${currentStep * 100}%)`;

        pages.forEach((page, index) => {
            const active = index === currentStep;

            page.setAttribute("aria-hidden", String(!active));
            page.inert = !active;
        });

        tabs.forEach((tab, index) => {
            const active = index === currentStep;

            tab.classList.toggle("active", active);

            if (active) {
                tab.setAttribute("aria-current", "step");
            } else {
                tab.removeAttribute("aria-current");
            }

            tab.disabled = index > maxStepReached;
        });

        requestAnimationFrame(() => {
            updateWizardHeight();
            scrollActiveTabIntoView();
        });
    }


    // ---------------------------------------------------------
    // VALIDATE CHECKBOX GROUPS
    // ---------------------------------------------------------
    function validateCheckboxGroups(page, report = true) {
        for (const name of requiredCheckboxGroups) {
            const checkboxes = [...page.querySelectorAll(`input[type="checkbox"][name="${name}"]`)];

            if (!checkboxes.length) continue;

            checkboxes.forEach(checkbox => checkbox.setCustomValidity(""));

            const selected = checkboxes.filter(checkbox => checkbox.checked);

            let target = null;
            let message = "";

            if (!selected.length) {
                target = checkboxes[0];
                message = "Please select at least one option.";
            } else if (name === "priority_areas" && selected.length > 3) {
                target = selected[selected.length - 1];
                message = "Please choose no more than three priorities.";
            }

            if (target) {
                target.setCustomValidity(message);

                if (report) {
                    target.reportValidity();
                    target.focus();
                }

                return false;
            }
        }

        return true;
    }


    // ---------------------------------------------------------
    // VALIDATE STEP
    // ---------------------------------------------------------
    function validateStep(step, report = true) {
        const page = pages[step];
        if (!page) return true;

        const fields = [...page.querySelectorAll("input, select, textarea")];

        // Clear previous checkbox-group validation messages.
        requiredCheckboxGroups.forEach(name => {
            page.querySelectorAll(`input[type="checkbox"][name="${name}"]`).forEach(
                checkbox => checkbox.setCustomValidity("")
            );
        });

        for (const field of fields) {
            if (field.disabled || field.type === "hidden") continue;

            if (!field.checkValidity()) {
                if (report) {
                    field.reportValidity();
                    field.focus();
                }

                return false;
            }
        }

        if (!validateCheckboxGroups(page, report)) return false;

        // Other accent is compulsory only when "Other" is selected.
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

            if (report) {
                accentOtherInput.reportValidity();
                accentOtherInput.focus();
            }

            return false;
        }

        if (accentOtherInput) accentOtherInput.setCustomValidity("");

        return true;
    }


    // ---------------------------------------------------------
    // OTHER ACCENT / VARIETY
    // ---------------------------------------------------------
    function updateAccentOtherField() {
        if (!accentOtherCheckbox || !accentOtherField || !accentOtherInput) return;

        const show = accentOtherCheckbox.checked;

        accentOtherField.hidden = !show;

        if (!show) {
            accentOtherInput.value = "";
            accentOtherInput.setCustomValidity("");
        }

        requestAnimationFrame(updateWizardHeight);
    }


    // ---------------------------------------------------------
    // NEXT
    // ---------------------------------------------------------
    nextButtons.forEach(button => {
        button.addEventListener("click", () => {
            if (!validateStep(currentStep)) return;

            maxStepReached = Math.max(maxStepReached, currentStep + 1);
            showStep(currentStep + 1);
        });
    });


    // ---------------------------------------------------------
    // BACK
    // ---------------------------------------------------------
    backButtons.forEach(button => {
        button.addEventListener("click", () => {
            showStep(currentStep - 1);
        });
    });


    // ---------------------------------------------------------
    // PROGRESS NAVIGATION
    // ---------------------------------------------------------
    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            if (index <= maxStepReached) showStep(index);
        });
    });


    // ---------------------------------------------------------
    // CHECKBOX VALIDATION RESET
    // ---------------------------------------------------------
    requiredCheckboxGroups.forEach(name => {
        const checkboxes = [...form.querySelectorAll(`input[type="checkbox"][name="${name}"]`)];

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener("change", () => {
                checkboxes.forEach(item => item.setCustomValidity(""));
            });
        });
    });


    // ---------------------------------------------------------
    // ACCENT EVENTS
    // ---------------------------------------------------------
    if (accentOtherCheckbox) {
        accentOtherCheckbox.addEventListener("change", updateAccentOtherField);
    }

    if (accentOtherInput) {
        accentOtherInput.addEventListener("input", () => {
            accentOtherInput.setCustomValidity("");
        });
    }


    // ---------------------------------------------------------
    // FINAL SUBMISSION — VALIDATE ALL STEPS
    // ---------------------------------------------------------
    form.addEventListener("submit", event => {
        for (let index = 0; index < pages.length; index++) {
            if (!validateStep(index, false)) {
                event.preventDefault();

                maxStepReached = Math.max(maxStepReached, index);
                showStep(index);

                requestAnimationFrame(() => validateStep(index));

                return;
            }
        }
    });


    // ---------------------------------------------------------
    // RESIZE
    // ---------------------------------------------------------
    window.addEventListener("resize", updateWizardHeight);


    // ---------------------------------------------------------
    // RESTORE FIRST STEP WITH SERVER-SIDE ERRORS
    // ---------------------------------------------------------
    const firstErrorStep = pages.findIndex(page =>
        page.querySelector(".needs-analysis-field--error, .needs-analysis-field__errors")
    );

    if (firstErrorStep >= 0) {
        currentStep = firstErrorStep;
        maxStepReached = firstErrorStep;
    }

    updateAccentOtherField();
    showStep(currentStep);
});