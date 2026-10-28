    document
        .querySelectorAll(".training-attendance-bar-fill")
        .forEach((bar) => {

            const percentage =
                parseFloat(bar.dataset.percentage) || 0;

            bar.style.width =
                `${Math.min(Math.max(percentage, 0), 100)}%`;
        });




        const todayClassesList =
    document.querySelector(".today-classes-list");

if (todayClassesList) {

    function updateTodayClassesScrollbar() {

        const hasVerticalOverflow =
            todayClassesList.scrollHeight >
            todayClassesList.clientHeight;

        todayClassesList.classList.toggle(
            "is-scrollable",
            hasVerticalOverflow
        );
    }

    updateTodayClassesScrollbar();

    window.addEventListener(
        "resize",
        updateTodayClassesScrollbar
    );
}