// =========================================================
// COURSES PAGE
// Course status filtering
// Desktop buttons + mobile custom dropdown
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const statusInput =
        document.getElementById("courseStatusFilter");

    const statusButtons =
        document.querySelectorAll(".course-status-btn");

    const courseRows =
        document.querySelectorAll(".assigned-course-row");

    const noCoursesFilterMessage =
        document.getElementById("noCoursesFilterMessage");


    /* Custom mobile dropdown */
    const dropdownToggle =
        document.getElementById("courseStatusDropdownToggle");

    const dropdownCurrent =
        document.getElementById("courseStatusDropdownCurrent");

    const dropdownCount =
        document.getElementById("courseStatusDropdownCount");

    const dropdownMenu =
        document.getElementById("courseStatusDropdownMenu");

    const dropdownOptions =
        document.querySelectorAll(
            ".course-status-dropdown-option"
        );


    if (!statusInput) {
        return;
    }


    const defaultStatus = "active";


    /* -----------------------------------------------------
       DESKTOP BUTTON STATE
    ----------------------------------------------------- */

    function setActiveStatusButton(selectedStatus) {

        statusButtons.forEach(function (button) {

            const isActive =
                button.dataset.status === selectedStatus;

            button.classList.toggle(
                "active",
                isActive
            );

            button.setAttribute(
                "aria-pressed",
                isActive ? "true" : "false"
            );
        });
    }


    /* -----------------------------------------------------
       MOBILE DROPDOWN STATE
    ----------------------------------------------------- */

    function setActiveDropdownOption(selectedStatus) {

        dropdownOptions.forEach(function (option) {

            const isActive =
                option.dataset.status === selectedStatus;

            option.classList.toggle(
                "active",
                isActive
            );

            option.setAttribute(
                "aria-pressed",
                isActive ? "true" : "false"
            );


            if (isActive) {

                if (dropdownCurrent) {
                    dropdownCurrent.textContent =
                        option.dataset.label;
                }

                if (dropdownCount) {
                    dropdownCount.textContent =
                        option.dataset.count;
                }
            }
        });


        statusInput.value =
            selectedStatus;
    }


    /* -----------------------------------------------------
       FILTER COURSES
    ----------------------------------------------------- */

    function applyStatusFilter(selectedStatus) {

        let visibleRows = 0;


        courseRows.forEach(function (row) {

            const rowStatus =
                row.dataset.status;

            const shouldShow =
                selectedStatus === "all" ||
                rowStatus === selectedStatus;


            row.classList.toggle(
                "course-hidden",
                !shouldShow
            );


            if (shouldShow) {
                visibleRows++;
            }
        });


        if (noCoursesFilterMessage) {

            noCoursesFilterMessage.hidden =
                visibleRows > 0;
        }


        /* Keep desktop + mobile controls synchronized */
        setActiveStatusButton(
            selectedStatus
        );

        setActiveDropdownOption(
            selectedStatus
        );
    }


    /* -----------------------------------------------------
       DROPDOWN OPEN / CLOSE
    ----------------------------------------------------- */

    function openDropdown() {

        if (
            !dropdownMenu ||
            !dropdownToggle
        ) {
            return;
        }

        dropdownMenu.hidden = false;

        dropdownToggle.setAttribute(
            "aria-expanded",
            "true"
        );
    }


    function closeDropdown() {

        if (
            !dropdownMenu ||
            !dropdownToggle
        ) {
            return;
        }

        dropdownMenu.hidden = true;

        dropdownToggle.setAttribute(
            "aria-expanded",
            "false"
        );
    }


    function toggleDropdown() {

        if (!dropdownMenu) {
            return;
        }

        if (dropdownMenu.hidden) {
            openDropdown();
        } else {
            closeDropdown();
        }
    }


    /* -----------------------------------------------------
       MOBILE TOGGLE
    ----------------------------------------------------- */

    if (dropdownToggle) {

        dropdownToggle.addEventListener(
            "click",
            function () {
                toggleDropdown();
            }
        );
    }


    /* -----------------------------------------------------
       MOBILE OPTIONS
    ----------------------------------------------------- */

    dropdownOptions.forEach(function (option) {

        option.addEventListener(
            "click",
            function () {

                const selectedStatus =
                    this.dataset.status;

                applyStatusFilter(
                    selectedStatus
                );

                closeDropdown();

                if (dropdownToggle) {
                    dropdownToggle.focus();
                }
            }
        );
    });


    /* -----------------------------------------------------
       DESKTOP FILTER BUTTONS
    ----------------------------------------------------- */

    statusButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                applyStatusFilter(
                    this.dataset.status
                );
            }
        );
    });


    /* -----------------------------------------------------
       CLICK OUTSIDE
    ----------------------------------------------------- */

    document.addEventListener(
        "click",
        function (event) {

            if (
                !dropdownToggle ||
                !dropdownMenu
            ) {
                return;
            }


            const dropdown =
                dropdownToggle.closest(
                    ".course-status-dropdown"
                );


            if (
                dropdown &&
                !dropdown.contains(event.target)
            ) {
                closeDropdown();
            }
        }
    );


    /* -----------------------------------------------------
       ESCAPE KEY
    ----------------------------------------------------- */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                dropdownMenu &&
                !dropdownMenu.hidden
            ) {
                closeDropdown();

                if (dropdownToggle) {
                    dropdownToggle.focus();
                }
            }
        }
    );


    /* -----------------------------------------------------
       INITIAL STATE
    ----------------------------------------------------- */

    applyStatusFilter(
        defaultStatus
    );

});