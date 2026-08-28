    // COURSE SELECTOR FORM - Dropdown element
    
    document.addEventListener("DOMContentLoaded", function () {

    const dropdowns =
        document.querySelectorAll(".course-dropdown");

    dropdowns.forEach(function (dropdown) {

        const toggle =
            dropdown.querySelector(".course-dropdown-toggle");

        const menu =
            dropdown.querySelector(".course-dropdown-menu");

        if (!toggle || !menu) {
            return;
        }


        /* =============================================
           OPEN / CLOSE DROPDOWN
        ============================================= */

        toggle.addEventListener("click", function (event) {

            event.stopPropagation();

            const isOpen =
                toggle.getAttribute("aria-expanded") === "true";

            toggle.setAttribute(
                "aria-expanded",
                isOpen ? "false" : "true"
            );

            menu.hidden = isOpen;

            dropdown.classList.toggle(
                "open",
                !isOpen
            );

        });


        /* =============================================
           CLOSE WHEN CLICKING OUTSIDE
        ============================================= */

        document.addEventListener("click", function (event) {

            if (!dropdown.contains(event.target)) {

                toggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                menu.hidden = true;

                dropdown.classList.remove("open");

            }

        });


        /* =============================================
           ESCAPE KEY
        ============================================= */

        toggle.addEventListener("keydown", function (event) {

            if (event.key === "Escape") {

                toggle.setAttribute(
                    "aria-expanded",
                    "false"
                );

                menu.hidden = true;

                dropdown.classList.remove("open");

                toggle.focus();

            }

        });

    });

});
