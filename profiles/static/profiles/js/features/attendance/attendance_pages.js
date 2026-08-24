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