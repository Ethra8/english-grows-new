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

           Supports BOTH:

           - <button type="submit">
           - <a href="...">

           We do NOT use preventDefault() here.

           Therefore:
           - submit buttons submit normally
           - links navigate normally
        --------------------------------------------------------- */

        const options =
            dropdown.querySelectorAll(
                ".course-dropdown-option"
            );


        options.forEach(function (option) {

            option.addEventListener(
                "click",
                function () {

                    toggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );


                    menu.hidden = true;


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
   COURSE ATTENDANCE FILTERS

   Used on the Company Admin course attendance page.

   Filters submitted attendance rows by:

   - class date
   - employee name / username / email

   Both filters can be used together.
========================================================= */

function initCourseAttendanceFilters() {

    const attendanceList =
        document.querySelector(".attendance-list");

    const dateFilter =
        document.getElementById("attendanceDateFilter");

    const searchInput =
        document.getElementById("attendanceSearchInput");


    /*
        This JS file is shared across pages.

        If the current page does not contain an attendance
        list, simply stop here.
    */

    if (!attendanceList) {
        return;
    }


    const attendanceRows =
        Array.from(
            attendanceList.querySelectorAll(
                ".attendance-row"
            )
        );


    if (!attendanceRows.length) {
        return;
    }


    /* ---------------------------------------------------------
       EMPTY FILTER RESULT MESSAGE

       This is separate from Django's {% empty %} message.

       Django's message means:
           there are no attendance records at all.

       This JS message means:
           records exist, but none match the current filters.
    --------------------------------------------------------- */

    let filterEmptyMessage =
        attendanceList.querySelector(
            ".attendance-filter-empty-message"
        );


    if (!filterEmptyMessage) {

        filterEmptyMessage =
            document.createElement("p");

        filterEmptyMessage.className =
            "attendance-empty-message attendance-filter-empty-message";

        filterEmptyMessage.textContent =
            "No attendance records match the selected filters.";

        filterEmptyMessage.hidden = true;

        attendanceList.appendChild(
            filterEmptyMessage
        );

    }


    /* ---------------------------------------------------------
       NORMALIZE TEXT
    --------------------------------------------------------- */

    function normalizeText(value) {

        return (value || "")
            .toLowerCase()
            .trim();

    }


    /* ---------------------------------------------------------
       APPLY FILTERS
    --------------------------------------------------------- */

    function applyAttendanceFilters() {

        const selectedDate =
            dateFilter
                ? dateFilter.value
                : "";


        const searchTerm =
            searchInput
                ? normalizeText(searchInput.value)
                : "";


        let visibleRows = 0;


        attendanceRows.forEach(function (row) {

            const rowDate =
                row.dataset.date || "";


            const rowSearch =
                normalizeText(
                    row.dataset.search
                );


            /* ---------------------------------------------
               DATE MATCH
            --------------------------------------------- */

            const matchesDate =
                !selectedDate
                || rowDate === selectedDate;


            /* ---------------------------------------------
               EMPLOYEE SEARCH MATCH

               data-search already contains:
               - full name
               - username
               - email

               for all attendance records assigned to
               that ClassSession.
            --------------------------------------------- */

            const matchesSearch =
                !searchTerm
                || rowSearch.includes(searchTerm);


            /* ---------------------------------------------
               FINAL RESULT
            --------------------------------------------- */

            const shouldShow =
                matchesDate
                && matchesSearch;


            row.hidden =
                !shouldShow;


            if (shouldShow) {
                visibleRows += 1;
            }

        });


        /* ---------------------------------------------
           NO RESULTS MESSAGE
        --------------------------------------------- */

        filterEmptyMessage.hidden =
            visibleRows !== 0;

    }


    /* ---------------------------------------------------------
       DATE FILTER
    --------------------------------------------------------- */

    if (dateFilter) {

        dateFilter.addEventListener(
            "change",
            applyAttendanceFilters
        );

    }


    /* ---------------------------------------------------------
       EMPLOYEE SEARCH

       "input" updates immediately while typing.
    --------------------------------------------------------- */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            applyAttendanceFilters
        );

    }


    /* ---------------------------------------------------------
       INITIAL STATE
    --------------------------------------------------------- */

    applyAttendanceFilters();

}


/* =========================================================
   INITIALIZE
========================================================= */

function initCourseComponents() {

    initCourseDropdowns();

    initCourseAttendanceFilters();

}


if (document.readyState === "loading") {

    document.addEventListener(
        "DOMContentLoaded",
        initCourseComponents
    );

} else {

    initCourseComponents();

}