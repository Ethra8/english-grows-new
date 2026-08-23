// GO TO PREVIOUS PAGE -- GO BACK
document.addEventListener("DOMContentLoaded", function () {
    const backLinks = document.querySelectorAll(".js-back-link");

    backLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();

            if (window.history.length > 1) {
                window.history.back();
            } else {
                window.location.href = "/";
            }
        });
    });
});



// COMPANY ADMIN COURSE ATTENDANCE FILTERS
// for company_admin_course_attendance.html
document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".attendance-filter-btn");
    const rows = document.querySelectorAll(".attendance-row");
    const dateFilter = document.getElementById("attendanceDateFilter");
    const searchInput = document.getElementById("attendanceSearchInput");
    const noResultsMessage = document.getElementById("attendanceNoResults");
    const title = document.getElementById("attendanceListTitle");

    if (rows.length === 0) {
        return;
    }

    let activeFilter = "completed";

    function updateTitle() {
        if (!title) return;

        title.textContent = "Submitted Attendance";
    }

    function applyFilters() {
        const selectedDate = dateFilter ? dateFilter.value : "";
        const searchValue = searchInput
            ? searchInput.value.trim().toLowerCase()
            : "";

        let visibleCount = 0;

        rows.forEach(function (row) {
            const rowStatus = row.dataset.status || "";
            const rowDate = row.dataset.date || "";
            const rowSearch = row.dataset.search || "";

            const matchesStatus =
                activeFilter === "all" || rowStatus === activeFilter;

            const matchesDate =
                !selectedDate || rowDate === selectedDate;

            const matchesSearch =
                !searchValue || rowSearch.includes(searchValue);

            const shouldShow =
                matchesStatus && matchesDate && matchesSearch;

            row.style.display = shouldShow ? "" : "none";

            if (shouldShow) {
                visibleCount++;
            }
        });

        if (noResultsMessage) {
            noResultsMessage.classList.toggle("d-none", visibleCount > 0);
        }

        updateTitle();
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            activeFilter = button.dataset.filter || "completed";

            filterButtons.forEach(function (btn) {
                btn.classList.remove("active");
            });

            button.classList.add("active");

            applyFilters();
        });
    });

    if (dateFilter) {
        dateFilter.addEventListener("change", applyFilters);
    }

    if (searchInput) {
        searchInput.addEventListener("input", applyFilters);
    }

    applyFilters();
});



// COMPANY ADMIN — GLOBAL ATTENDANCE BY COURSE
document.addEventListener("DOMContentLoaded", function () {
    const courseList = document.getElementById(
        "globalCourseAttendanceList"
    );

    // Do not run this code on other company-admin pages.
    if (!courseList) {
        return;
    }

    const rows = courseList.querySelectorAll(
        ".course-attendance-row"
    );

    const noResultsMessage = document.getElementById(
        "attendanceNoResults"
    );

    // Filtering is performed server-side by the Django GET form.
    // The JavaScript must not hide the returned course rows.
    rows.forEach(function (row) {
        row.style.display = "";
    });

    if (noResultsMessage) {
        noResultsMessage.classList.toggle(
            "d-none",
            rows.length > 0
        );
    }
});