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



// COURSES Page
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



// ATTENDANCE page
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
