// Function to render Teacher ASSIGNED COURSES on teacher_courses page
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


// Function to render Teacher CLASSES LIST on teacher_classes_list page
// depending on selected period from desktop buttons or mobile select
document.addEventListener("DOMContentLoaded", function () {
    const filter = document.getElementById("classesListFilter");
    const filterButtons = document.querySelectorAll(".classes-filter-btn");
    const rows = document.querySelectorAll(".assigned-class-row");
    const noClassesMessage = document.getElementById("noClassesMessage");

    if (!filter || rows.length === 0) {
        return;
    }

    function setActiveButton(selectedFilter) {
        filterButtons.forEach(function (button) {
            button.classList.toggle(
                "active",
                button.dataset.filter === selectedFilter
            );
        });
    }

    function rowMatchesFilter(row, selectedFilter) {
        if (selectedFilter === "all") {
            return true;
        }

        if (row.dataset.period === selectedFilter) {
            return true;
        }

        if (row.dataset[selectedFilter] === "true") {
            return true;
        }

        return false;
    }

    function applyClassFilter() {
        const selectedFilter = filter.value;
        let visibleRows = 0;

        rows.forEach(function (row) {
            const shouldShow = rowMatchesFilter(row, selectedFilter);

            row.hidden = !shouldShow;

            if (shouldShow) {
                visibleRows++;
            }
        });

        if (noClassesMessage) {
            noClassesMessage.hidden = visibleRows > 0;
        }

        setActiveButton(selectedFilter);
    }

    filter.addEventListener("change", applyClassFilter);

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            filter.value = button.dataset.filter;
            applyClassFilter();
        });
    });

    applyClassFilter();
});



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