document.addEventListener("DOMContentLoaded", function () {
    const attendanceGrid = document.querySelector(
        ".attendance-cards-grid"
    );

    const attendanceCard = document.querySelector(
        ".wrapper-attendance-details .detailed-attendance-card"
    );

    const absenceCard = document.querySelector(
        ".wrapper-absence-details .detailed-attendance-card"
    );

    const absenceCollapse = $("#parentAbsenceCollapse");

    if (
        !attendanceGrid ||
        !attendanceCard ||
        !absenceCard ||
        !absenceCollapse.length
    ) {
        return;
    }


    /*
     * BEFORE Bootstrap starts opening the accordion:
     *
     * Both cards are currently equal-height because the
     * CSS Grid is using align-items: stretch.
     *
     * We record that exact height and freeze the
     * Attendance card at that value.
     */
    absenceCollapse.on("show.bs.collapse", function () {
        const foldedHeight = absenceCard.getBoundingClientRect().height;

        attendanceCard.style.height = `${foldedHeight}px`;

        attendanceGrid.classList.add("absence-expanded");
    });


    /*
     * AFTER Bootstrap has completely closed the accordion:
     *
     * Restore normal CSS Grid behaviour.
     *
     * Removing the inline height lets the two cards become
     * equal-height naturally again.
     */
    absenceCollapse.on("hidden.bs.collapse", function () {
        attendanceGrid.classList.remove("absence-expanded");

        attendanceCard.style.height = "";
    });
});


// ATTENDANCE FILTER FORM 
// For ROLES: 
// - Company Admin: company_admin_course_attendance
// - Teacher: teacher_attendance

document.querySelectorAll(".attendance-row[data-url]").forEach(row => {
    row.addEventListener("click", event => {
        if (event.target.closest("a, button, input, select")) return;
        window.location.href = row.dataset.url;
    });
});


document.querySelectorAll('.attendance-date-picker-btn').forEach(button => {
    button.addEventListener('click', () => {
        const input = button.previousElementSibling;

        if (typeof input.showPicker === 'function') {
            input.showPicker();
        } else {
            input.focus();
            input.click();
        }
    });
});


// ATTENDANCE FILTERS for both Teacher & Admin
document.addEventListener("DOMContentLoaded", function () {
    const page = document.querySelector("[data-attendance-page]");
    if (!page) return;

    const filterButtons = page.querySelectorAll(".attendance-filter-btn");
    const rows = page.querySelectorAll(".attendance-row");
    const searchInput = page.querySelector("#attendanceSearchInput");
    const dateInput = page.querySelector("#attendanceDateFilter");
    const noResultsMessage = page.querySelector("#attendanceNoResults");
    const listTitle = page.querySelector("#attendanceListTitle");

    let activeFilter = page.dataset.defaultFilter || "completed";

    function applyFilters() {
        const searchValue = searchInput ? searchInput.value.trim().toLowerCase() : "";
        const selectedDate = dateInput ? dateInput.value : "";
        let visibleCount = 0;

        rows.forEach(function (row) {
            const rowStatus = row.dataset.status || "";
            const rowDate = row.dataset.date || "";
            const rowSearch = (row.dataset.search || "").toLowerCase();

            const matchesStatus = activeFilter === "all" || rowStatus === activeFilter;
            const matchesDate = !selectedDate || rowDate === selectedDate;
            const matchesSearch = !searchValue || rowSearch.includes(searchValue);
            const shouldShow = matchesStatus && matchesDate && matchesSearch;

            row.classList.toggle("course-hidden", !shouldShow);
            if (shouldShow) visibleCount++;
        });

        if (noResultsMessage) {
            noResultsMessage.classList.toggle("d-none", visibleCount > 0);
        }

        if (listTitle) {
            const activeButton = [...filterButtons].find(button => button.dataset.filter === activeFilter);
            if (activeButton?.dataset.listTitle) listTitle.textContent = activeButton.dataset.listTitle;
        }
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            activeFilter = this.dataset.filter;

            filterButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            applyFilters();
        });
    });

    searchInput?.addEventListener("input", applyFilters);
    dateInput?.addEventListener("change", applyFilters);

    applyFilters();
});