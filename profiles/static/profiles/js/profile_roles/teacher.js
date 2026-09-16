// CLASSES LIST Selector buttons & select element
document.addEventListener("DOMContentLoaded", function () {
    const panels = document.querySelectorAll(".assigned-classes-panel");

    panels.forEach(function (panel) {
        const filterButtons = panel.querySelectorAll(".classes-filter-btn");
        const mobileSelect = panel.querySelector(".classes-panel-select");
        const rows = panel.querySelectorAll(".assigned-class-row");
        const noClassesMessage = panel.querySelector(".no-classes-message");

        function applyPanelFilter(selectedFilter) {
            let visibleRows = 0;

            rows.forEach(function (row) {
                const shouldShow =
                    selectedFilter === "all" ||
                    row.dataset[selectedFilter] === "true";

                row.classList.toggle("class-hidden", !shouldShow);

                if (shouldShow) {
                    visibleRows++;
                }
            });

            filterButtons.forEach(function (button) {
                button.classList.toggle(
                    "active",
                    button.dataset.filter === selectedFilter
                );
            });

            if (mobileSelect) {
                mobileSelect.value = selectedFilter;
            }

            if (noClassesMessage) {
                noClassesMessage.hidden = visibleRows > 0;
            }
        }

        filterButtons.forEach(function (button) {
            button.addEventListener("click", function (event) {
                event.stopPropagation();
                applyPanelFilter(button.dataset.filter);
            });
        });

        if (mobileSelect) {
            mobileSelect.addEventListener("change", function (event) {
                event.stopPropagation();
                applyPanelFilter(event.target.value);
            });
        }
        // today upcoming classes is pre-selected on page load
        applyPanelFilter("today");
    });
});


// TAKE ATTENDANCE Page
document.addEventListener("DOMContentLoaded", function () {
    const markAllButtons = document.querySelectorAll(".mark-all-btn");

    markAllButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const status = button.getAttribute("data-status");

            const radios = document.querySelectorAll(
                `input[type="radio"][value="${status}"]`
            );


            console.log(status);
            console.log(radios);

            radios.forEach(function (radio) {
                radio.checked = true;
            });
        });
    });
});


// UPDATE STUDENT LEVEL Form
function toggleLevelForm(enrollmentId) {
    const form = document.getElementById(`level-form-${enrollmentId}`);

    if (!form) {
        return;
    }

    form.classList.toggle("d-none");
}


// Class List page:
// Reschedule MODAL to Confirm/Cancel Reschedule Action
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("rescheduleModal");
    const cancelButton = document.getElementById("cancelRescheduleModal");
    const confirmForm = document.getElementById("rescheduleConfirmForm");
    const classNameText = document.getElementById("rescheduleModalClassName");
    const openButtons = document.querySelectorAll(".js-open-reschedule-modal");

    if (!modal || !cancelButton || !confirmForm) {
        return;
    }

    openButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const actionUrl = button.dataset.actionUrl;
            const classTitle = button.dataset.classTitle;

            confirmForm.setAttribute("action", actionUrl);
            classNameText.textContent = classTitle;

            modal.classList.add("is-visible");
        });
    });

    cancelButton.addEventListener("click", function () {
        modal.classList.remove("is-visible");
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.classList.remove("is-visible");
        }
    });
});