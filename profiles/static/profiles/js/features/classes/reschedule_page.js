document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       RESCHEDULE PAGE
       Shared by:
       - Teacher
       - Employee
       - Learner
    ========================================================= */


    /* =========================================================
       HELPERS
    ========================================================= */

    function datasetIsTrue(value) {
        return (
            value === "true" ||
            value === "True" ||
            value === "1"
        );
    }


    /* =========================================================
       MAIN TABS
       Pending Reschedule / Rescheduled
    ========================================================= */

    const statusTabs =
        document.querySelectorAll(".reschedule-page-tab");

    const statusPanels =
        document.querySelectorAll(".reschedule-page-panel");


    if (statusTabs.length && statusPanels.length) {

        statusTabs.forEach(function (tab) {

            tab.addEventListener("click", function () {

                const targetId = tab.dataset.target;


                /* -----------------------------------------
                   Update tab state
                ----------------------------------------- */

                statusTabs.forEach(function (otherTab) {

                    const isActive =
                        otherTab === tab;

                    otherTab.classList.toggle(
                        "active",
                        isActive
                    );

                    otherTab.setAttribute(
                        "aria-selected",
                        isActive ? "true" : "false"
                    );

                });


                /* -----------------------------------------
                   Show correct panel
                ----------------------------------------- */

                statusPanels.forEach(function (panel) {

                    const isTarget =
                        panel.id === targetId;

                    panel.hidden = !isTarget;

                    panel.classList.toggle(
                        "active",
                        isTarget
                    );

                });

            });

        });

    }


    /* =========================================================
       RESCHEDULED FILTERS
       Upcoming / Past / All

       Upcoming:
       start_time >= now

       Past:
       start_time < now
    ========================================================= */

    const rescheduledPanel =
        document.getElementById("rescheduled-panel");


    if (rescheduledPanel) {

        const filterButtons =
            rescheduledPanel.querySelectorAll(
                ".reschedule-page-filter-btn"
            );

        const rows =
            rescheduledPanel.querySelectorAll(
                ".reschedule-page-row[data-rescheduled-past]"
            );

        const noResultsMessage =
            rescheduledPanel.querySelector(
                ".reschedule-page-filter-empty"
            );


        function applyRescheduledFilter(filter) {

            let visibleRows = 0;


            rows.forEach(function (row) {

                let shouldShow = false;


                switch (filter) {

                    case "upcoming":
                        shouldShow =
                            datasetIsTrue(
                                row.dataset.rescheduledUpcoming
                            );
                        break;


                    case "past":
                        shouldShow =
                            datasetIsTrue(
                                row.dataset.rescheduledPast
                            );
                        break;


                    case "all":
                        shouldShow = true;
                        break;


                    default:
                        shouldShow = true;
                }


                row.classList.toggle(
                    "reschedule-page-row-hidden",
                    !shouldShow
                );


                if (shouldShow) {
                    visibleRows++;
                }

            });


            /* -----------------------------------------
               Update filter button state
            ----------------------------------------- */

            filterButtons.forEach(function (button) {

                const isActive =
                    button.dataset.rescheduledFilter === filter;

                button.classList.toggle(
                    "active",
                    isActive
                );

                button.setAttribute(
                    "aria-selected",
                    isActive ? "true" : "false"
                );

            });


            /* -----------------------------------------
               Empty-state message
            ----------------------------------------- */

            if (noResultsMessage) {
                noResultsMessage.hidden =
                    visibleRows > 0;
            }

        }


        /* ---------------------------------------------
           Filter button listeners
        --------------------------------------------- */

        filterButtons.forEach(function (button) {

            button.addEventListener("click", function () {

                const filter =
                    button.dataset.rescheduledFilter;

                applyRescheduledFilter(filter);

            });

        });


        /* ---------------------------------------------
           Default filter
        --------------------------------------------- */

        if (filterButtons.length) {
            applyRescheduledFilter("upcoming");
        }

    }


    /* =========================================================
       RESCHEDULE CONFIRMATION MODAL

       This section only runs if the page contains:
       #rescheduleModal
       #rescheduleConfirmForm

       Teacher HTML:
       can include these

       Learner / Employee HTML:
       can omit them completely
    ========================================================= */

    const modal =
        document.getElementById("rescheduleModal");

    const cancelButton =
        document.getElementById("cancelRescheduleModal");

    const confirmForm =
        document.getElementById("rescheduleConfirmForm");

    const classNameText =
        document.getElementById("rescheduleModalClassName");

    const classTimeText =
        document.getElementById("rescheduleModalClassTime");


    function closeRescheduleModal() {

        if (!modal) {
            return;
        }

        modal.classList.remove("is-visible");


        if (confirmForm) {
            confirmForm.removeAttribute("action");
        }


        if (classNameText) {
            classNameText.textContent = "";
        }


        if (classTimeText) {
            classTimeText.textContent = "";
        }

    }


    if (
        modal &&
        cancelButton &&
        confirmForm
    ) {

        /* ---------------------------------------------
           Open modal

           Event delegation is used so any future
           .js-open-reschedule-modal button also works.
        --------------------------------------------- */

        document.addEventListener("click", function (event) {

            const button =
                event.target.closest(
                    ".js-open-reschedule-modal"
                );

            if (!button) {
                return;
            }


            const actionUrl =
                button.dataset.actionUrl;

            const classTitle =
                button.dataset.classTitle;

            const classDate =
                button.dataset.classDate;

            const classTime =
                button.dataset.classTime;


            /* -----------------------------------------
               Set form action
            ----------------------------------------- */

            if (actionUrl) {

                confirmForm.setAttribute(
                    "action",
                    actionUrl
                );

            }


            /* -----------------------------------------
               Populate modal information
            ----------------------------------------- */

            if (classNameText) {

                classNameText.textContent =
                    classTitle || "";

            }


            if (classTimeText) {

                const dateTimeParts = [];


                if (classDate) {
                    dateTimeParts.push(classDate);
                }


                if (classTime) {
                    dateTimeParts.push(classTime);
                }


                classTimeText.textContent =
                    dateTimeParts.join(" | ");

            }


            /* -----------------------------------------
               Show modal
            ----------------------------------------- */

            modal.classList.add("is-visible");

        });


        /* ---------------------------------------------
           Cancel button
        --------------------------------------------- */

        cancelButton.addEventListener("click", function () {
            closeRescheduleModal();
        });


        /* ---------------------------------------------
           Click outside modal
        --------------------------------------------- */

        modal.addEventListener("click", function (event) {

            if (event.target === modal) {
                closeRescheduleModal();
            }

        });


        /* ---------------------------------------------
           Escape key
        --------------------------------------------- */

        document.addEventListener("keydown", function (event) {

            if (
                event.key === "Escape" &&
                modal.classList.contains("is-visible")
            ) {
                closeRescheduleModal();
            }

        });

    }

});