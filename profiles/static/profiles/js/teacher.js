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

    if (!filter) {
        return;
    }

    function setActiveButton(selectedPeriod) {
        filterButtons.forEach(function (button) {
            if (button.dataset.filter === selectedPeriod) {
                button.classList.add("active");
            } else {
                button.classList.remove("active");
            }
        });
    }

    function applyClassFilter() {
        const selectedPeriod = filter.value;
        let visibleRows = 0;

        rows.forEach(function (row) {
            const rowPeriod = row.getAttribute("data-period");
            const rowMatchesSelectedPeriod =
                row.getAttribute(`data-${selectedPeriod}`) === "true";

            if (
                selectedPeriod === "all" ||
                rowPeriod === selectedPeriod ||
                rowMatchesSelectedPeriod
            ) {
                row.classList.remove("class-hidden");
                visibleRows++;
            } else {
                row.classList.add("class-hidden");
            }
        });

        if (noClassesMessage) {
            if (visibleRows === 0) {
                noClassesMessage.classList.remove("class-hidden");
            } else {
                noClassesMessage.classList.add("class-hidden");
            }
        }

        setActiveButton(selectedPeriod);
    }

    filter.addEventListener("change", applyClassFilter);

    filterButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const selectedPeriod = button.dataset.filter;

            filter.value = selectedPeriod;
            applyClassFilter();
        });
    });

    applyClassFilter();
});