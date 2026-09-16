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