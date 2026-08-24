// =========================================================
// SKILL CARD ACCORDIONS
//
// Behaviour:
// - Initially all skill cards are collapsed.
// - Chart receives the height of the collapsed skills column.
// - Opening skill details grows ONLY the skills column.
// - Chart height remains unchanged.
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const skillsGrid = document.querySelector(
        ".skills-grid"
    );

    const accordionToggles = document.querySelectorAll(
        ".skill-accordion-toggle"
    );

    const chartSection = document.querySelector(
        ".skills-progress-section"
    );


    if (
        !skillsGrid ||
        !accordionToggles.length
    ) {
        return;
    }


    // ---------------------------------------------------------
    // STORE DEFAULT COLLAPSED CHART HEIGHT
    //
    // At page load all skill accordions are collapsed and
    // CSS Grid has made both columns equal height.
    //
    // Capture that exact height once.
    // ---------------------------------------------------------

    if (chartSection) {

        requestAnimationFrame(function () {

            const collapsedHeight =
                chartSection.getBoundingClientRect().height;


            if (collapsedHeight > 0) {

                chartSection.style.height =
                    `${collapsedHeight}px`;

                chartSection.style.flex =
                    "0 0 auto";
            }

        });

    }


    // ---------------------------------------------------------
    // ACCORDION CONTROLS
    // ---------------------------------------------------------

    accordionToggles.forEach(function (toggle) {

        toggle.addEventListener("click", function () {

            const bodyId = toggle.getAttribute(
                "aria-controls"
            );

            const body = document.getElementById(
                bodyId
            );


            if (!body) {
                return;
            }


            const isOpen = (
                toggle.getAttribute("aria-expanded")
                === "true"
            );


            toggle.setAttribute(
                "aria-expanded",
                isOpen ? "false" : "true"
            );


            body.hidden = isOpen;

        });

    });

});