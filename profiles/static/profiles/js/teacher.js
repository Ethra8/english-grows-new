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
// depending on WHEN in the <select> element
document.addEventListener("DOMContentLoaded", function () {
    const filter = document.getElementById("classesListFilter");
    const rows = document.querySelectorAll(".assigned-class-row");

    if (!filter || rows.length === 0) {
        return;
    }

    function applyClassFilter() {
        const selectedPeriod = filter.value;

        rows.forEach(function (row) {
            const rowPeriod = row.getAttribute("data-period");

            if (selectedPeriod === "all" || rowPeriod === selectedPeriod) {
                row.classList.remove("class-hidden");
            } else {
                row.classList.add("class-hidden");
            }
        });
    }

    filter.addEventListener("change", applyClassFilter);

    applyClassFilter();
});