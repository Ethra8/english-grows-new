/* =========================================================
   COURSE SELECTOR FORM — CUSTOM DROPDOWN
========================================================= */

function initCourseDropdowns() {

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


        /* ---------------------------------------------------------
           OPEN / CLOSE
        --------------------------------------------------------- */

        toggle.addEventListener("click", function (event) {

            event.preventDefault();
            event.stopPropagation();


            const isOpen =
                toggle.getAttribute("aria-expanded") === "true";


            /*
                Close every other dropdown first.
            */

            dropdowns.forEach(function (otherDropdown) {

                if (otherDropdown === dropdown) {
                    return;
                }


                const otherToggle =
                    otherDropdown.querySelector(
                        ".course-dropdown-toggle"
                    );

                const otherMenu =
                    otherDropdown.querySelector(
                        ".course-dropdown-menu"
                    );


                if (otherToggle) {
                    otherToggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );
                }


                if (otherMenu) {
                    otherMenu.hidden = true;
                }


                otherDropdown.classList.remove(
                    "open"
                );
            });


            /*
                Toggle current dropdown.
            */

            toggle.setAttribute(
                "aria-expanded",
                isOpen ? "false" : "true"
            );


            menu.hidden =
                isOpen;


            dropdown.classList.toggle(
                "open",
                !isOpen
            );

        });


        /* ---------------------------------------------------------
           COURSE OPTION CLICK

           The button is already type="submit", therefore the
           browser submits:

               ?course=<button value>

           We DO NOT preventDefault() here.
        --------------------------------------------------------- */

        const options =
            dropdown.querySelectorAll(
                ".course-dropdown-option"
            );


        options.forEach(function (option) {

            option.addEventListener(
                "click",
                function () {

                    /*
                        Do NOT use preventDefault here.

                        Allow normal form submission.
                    */

                    toggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );


                    dropdown.classList.remove(
                        "open"
                    );

                }
            );

        });


        /* ---------------------------------------------------------
           ESCAPE
        --------------------------------------------------------- */

        toggle.addEventListener(
            "keydown",
            function (event) {

                if (event.key !== "Escape") {
                    return;
                }


                menu.hidden = true;


                toggle.setAttribute(
                    "aria-expanded",
                    "false"
                );


                dropdown.classList.remove(
                    "open"
                );


                toggle.focus();

            }
        );

    });


    /* ---------------------------------------------------------
       CLICK OUTSIDE — CLOSE ALL
    --------------------------------------------------------- */

    document.addEventListener(
        "click",
        function (event) {

            dropdowns.forEach(function (dropdown) {

                if (dropdown.contains(event.target)) {
                    return;
                }


                const toggle =
                    dropdown.querySelector(
                        ".course-dropdown-toggle"
                    );


                const menu =
                    dropdown.querySelector(
                        ".course-dropdown-menu"
                    );


                if (toggle) {

                    toggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }


                if (menu) {

                    menu.hidden = true;

                }


                dropdown.classList.remove(
                    "open"
                );

            });

        }
    );

}


/* =========================================================
   INITIALIZE
========================================================= */

if (document.readyState === "loading") {

    document.addEventListener(
        "DOMContentLoaded",
        initCourseDropdowns
    );

} else {

    initCourseDropdowns();

}