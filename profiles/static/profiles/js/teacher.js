// Function for <select> to render Teacher ASSIGNED COURSES on teacher_courses page
// depending on STATUS in the *<select>* element
document.addEventListener("DOMContentLoaded", function () {
    const filter = document.getElementById("courseStatusFilter");
    const rows = document.querySelectorAll(".assigned-course-row");

    if (!filter || rows.length === 0) {
        return;
    }

    filter.addEventListener("change", function () {
        const selectedStatus = filter.value;

        rows.forEach(function (row) {
            const rowStatus = row.getAttribute("data-status");

            if (selectedStatus === "all" || rowStatus === selectedStatus) {
                row.classList.remove("course-hidden");
            } else {
                row.classList.add("course-hidden");
            }
        });
    });
});

// Function for larger devices - buttons filter Courses Assigned to teacher
document.addEventListener("DOMContentLoaded", function () {
    const statusSelect = document.getElementById("courseStatusFilter");
    const statusButtons = document.querySelectorAll(".course-status-btn");
    const courseRows = document.querySelectorAll(".assigned-course-row");
    const noCoursesFilterMessage = document.getElementById("noCoursesFilterMessage");

    if (!statusSelect) {
        return;
    }

    const defaultStatus = "active";

    function setActiveStatusButton(selectedStatus) {
        statusButtons.forEach(function (button) {
            button.classList.toggle(
                "active",
                button.dataset.status === selectedStatus
            );
        });
    }

    function applyStatusFilter(selectedStatus) {
        let visibleRows = 0;

        courseRows.forEach(function (row) {
            const rowStatus = row.dataset.status;

            const shouldShow =
                selectedStatus === "all" || rowStatus === selectedStatus;

            row.classList.toggle("course-hidden", !shouldShow);

            if (shouldShow) {
                visibleRows++;
            }
        });

        if (noCoursesFilterMessage) {
            noCoursesFilterMessage.hidden = visibleRows > 0;
        }

        statusSelect.value = selectedStatus;
        setActiveStatusButton(selectedStatus);
    }

    statusSelect.addEventListener("change", function () {
        applyStatusFilter(statusSelect.value);
    });

    statusButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            applyStatusFilter(button.dataset.status);
        });
    });

    applyStatusFilter(defaultStatus);
});


// Function to render Teacher CLASSES LIST on teacher_classes_list page
// Teacher classes list filter: desktop buttons + mobile select
document.addEventListener("DOMContentLoaded", function () {
    const filter = document.getElementById("classesListFilter");
    const rows = document.querySelectorAll(".assigned-class-row");

    if (!filter || rows.length === 0) {
        return;
    }

    filter.addEventListener("change", function () {
        const selectedFilter = filter.value;

        rows.forEach(function (row) {
            if (selectedFilter === "all") {
                row.classList.remove("class-hidden");
                return;
            }

            const rowValue = row.getAttribute("data-" + selectedFilter);

            if (rowValue === "true") {
                row.classList.remove("class-hidden");
            } else {
                row.classList.add("class-hidden");
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const panel = document.querySelector(".assigned-classes-panel");

    if (!panel) {
        return;
    }

    const mobileFilter = panel.querySelector("#classesListFilter");
    const filterButtons = panel.querySelectorAll(".classes-filter-btn");
    const rows = panel.querySelectorAll(".assigned-class-row");
    const noClassesMessage = panel.querySelector("#noClassesMessage");

    if (rows.length === 0) {
        return;
    }

    function rowMatchesFilter(row, selectedFilter) {
        if (selectedFilter === "all") {
            return true;
        }

        return row.dataset[selectedFilter] === "true";
    }

    function applyClassFilter(selectedFilter) {
        let visibleRows = 0;

        rows.forEach(function (row) {
            const shouldShow = rowMatchesFilter(row, selectedFilter);

            row.hidden = !shouldShow;

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

        if (mobileFilter) {
            mobileFilter.value = selectedFilter;
        }

        if (noClassesMessage) {
            noClassesMessage.hidden = visibleRows > 0;
        }
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const selectedFilter = button.dataset.filter;
            applyClassFilter(selectedFilter);
        });
    });

    if (mobileFilter) {
        mobileFilter.addEventListener("change", function (event) {
            const selectedFilter = event.target.value;
            applyClassFilter(selectedFilter);
        });
    }

    applyClassFilter("upcoming");
});



document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".attendance-filter-btn");
    const rows = document.querySelectorAll(".attendance-row");
    const searchInput = document.getElementById("attendanceSearchInput");
    const dateInput = document.getElementById("attendanceDateFilter");
    const noResultsMessage = document.getElementById("attendanceNoResults");
    const listTitle = document.getElementById("attendanceListTitle");

    let currentFilter = "pending";

    function applyAttendanceFilters() {
        const searchValue = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const selectedDate = dateInput ? dateInput.value : "";
        let visibleRows = 0;

        rows.forEach(function (row) {
            const rowStatus = row.getAttribute("data-status");
            const rowSearch = row.getAttribute("data-search") || "";
            const rowDate = row.getAttribute("data-date") || "";

            const matchesStatus = rowStatus === currentFilter;
            const matchesSearch = rowSearch.includes(searchValue);
            const matchesDate = selectedDate === "" || rowDate === selectedDate;

            if (matchesStatus && matchesSearch && matchesDate) {
                row.classList.remove("course-hidden");
                visibleRows++;
            } else {
                row.classList.add("course-hidden");
            }
        });

        if (listTitle) {
            listTitle.textContent =
                currentFilter === "pending"
                    ? "Pending Attendance"
                    : "Completed Attendance";
        }

        if (noResultsMessage) {
            if (visibleRows === 0) {
                noResultsMessage.classList.remove("d-none");
            } else {
                noResultsMessage.classList.add("d-none");
            }
        }
    }

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            filterButtons.forEach(function (btn) {
                btn.classList.remove("active");
            });

            button.classList.add("active");
            currentFilter = button.getAttribute("data-filter");

            applyAttendanceFilters();
        });
    });

    if (searchInput) {
        searchInput.addEventListener("input", applyAttendanceFilters);
    }

    if (dateInput) {
        dateInput.addEventListener("change", applyAttendanceFilters);
    }

    applyAttendanceFilters();
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

            radios.forEach(function (radio) {
                radio.checked = true;
            });
        });
    });
});