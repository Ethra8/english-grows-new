document.addEventListener("DOMContentLoaded", function () {

    /* =========================================================
       CLASS SESSIONS
       Upcoming / Past tabs + Today / Week / Month / All filters
    ========================================================= */

    const statusTabs =
        document.querySelectorAll(".classes-status-tab");

    const statusPanels =
        document.querySelectorAll(".classes-status-panel");


    /* ---------------------------------------------------------
       URL FILTER
    --------------------------------------------------------- */

    const urlParams =
        new URLSearchParams(window.location.search);

    const requestedFilter =
        urlParams.get("filter");

    const allowedFilters = [
        "today",
        "weekly",
        "monthly",
        "all",
    ];

    const initialFilter =
        allowedFilters.includes(requestedFilter)
            ? requestedFilter
            : "today";


    /* ---------------------------------------------------------
       HELPERS
    --------------------------------------------------------- */

    function datasetIsTrue(value) {
        return (
            value === "true" ||
            value === "True" ||
            value === "1"
        );
    }


    /* ---------------------------------------------------------
       APPLY FILTER TO ONE STATUS PANEL
    --------------------------------------------------------- */

    function applyFilter(panel, filter) {

        const rows =
            panel.querySelectorAll(".assigned-class-row");

        const noClassesMessage =
            panel.querySelector(".no-classes-message");

        let visibleRows = 0;


        rows.forEach(row => {

            let shouldShow = false;

            switch (filter) {

                case "today":
                    shouldShow =
                        datasetIsTrue(row.dataset.today);
                    break;

                case "weekly":
                    shouldShow =
                        datasetIsTrue(row.dataset.weekly);
                    break;

                case "monthly":
                    shouldShow =
                        datasetIsTrue(row.dataset.monthly);
                    break;

                case "all":
                    shouldShow = true;
                    break;

                default:
                    shouldShow = true;
            }


            row.classList.toggle(
                "class-hidden",
                !shouldShow
            );


            if (shouldShow) {
                visibleRows++;
            }

        });


        /* Empty-state message */
        if (noClassesMessage) {
            noClassesMessage.hidden =
                visibleRows !== 0;
        }
    }


    /* ---------------------------------------------------------
       UPDATE URL FILTER
    --------------------------------------------------------- */

    function updateUrlFilter(filter) {

        const url =
            new URL(window.location.href);

        url.searchParams.set(
            "filter",
            filter
        );

        window.history.replaceState(
            {},
            "",
            url
        );
    }


    /* ---------------------------------------------------------
       SET FILTER FOR ONE PANEL
    --------------------------------------------------------- */

    function setPanelFilter(
        panel,
        filter,
        updateUrl = false
    ) {

        const buttons =
            panel.querySelectorAll(".classes-filter-btn");

        const select =
            panel.querySelector(".classes-panel-select");


        /* Desktop buttons */
        buttons.forEach(button => {

            const isActive =
                button.dataset.filter === filter;

            button.classList.toggle(
                "active",
                isActive
            );

            button.setAttribute(
                "aria-selected",
                isActive ? "true" : "false"
            );

        });


        /* Mobile select */
        if (select) {
            select.value = filter;
        }


        /* Remember each panel's own active filter */
        panel.dataset.activeFilter = filter;


        /* Filter the rows */
        applyFilter(
            panel,
            filter
        );


        /* Update URL only after a user action */
        if (updateUrl) {
            updateUrlFilter(filter);
        }
    }


    /* ---------------------------------------------------------
       INITIALISE EACH STATUS PANEL
    --------------------------------------------------------- */

    statusPanels.forEach(panel => {

        const buttons =
            panel.querySelectorAll(".classes-filter-btn");

        const select =
            panel.querySelector(".classes-panel-select");


        /* Desktop filter buttons */
        buttons.forEach(button => {

            button.addEventListener(
                "click",
                function () {

                    setPanelFilter(
                        panel,
                        this.dataset.filter,
                        true
                    );

                }
            );

        });


        /* Mobile select */
        if (select) {

            select.addEventListener(
                "change",
                function () {

                    setPanelFilter(
                        panel,
                        this.value,
                        true
                    );

                }
            );

        }


        /*
         * Initial filter:
         *
         * If URL contains:
         * ?filter=weekly
         * ?filter=monthly
         * ?filter=all
         * ?filter=today
         *
         * use that filter.
         *
         * Otherwise default to Today.
         */
        setPanelFilter(
            panel,
            initialFilter
        );

    });


    /* ---------------------------------------------------------
       UPCOMING / PAST STATUS NAVIGATION
    --------------------------------------------------------- */

    function showStatusPanel(status) {

        /* Status tabs */
        statusTabs.forEach(tab => {

            const isActive =
                tab.dataset.statusTab === status;

            tab.classList.toggle(
                "active",
                isActive
            );

            tab.setAttribute(
                "aria-selected",
                isActive ? "true" : "false"
            );

        });


        /* Status panels */
        statusPanels.forEach(panel => {

            const isActive =
                panel.dataset.statusPanel === status;

            panel.classList.toggle(
                "active",
                isActive
            );

            panel.hidden = !isActive;


            /*
             * Reapply this panel's own filter whenever
             * the panel becomes visible.
             */
            if (isActive) {

                const activeFilter =
                    panel.dataset.activeFilter || "today";

                applyFilter(
                    panel,
                    activeFilter
                );
            }

        });

    }


    /* ---------------------------------------------------------
       STATUS TAB EVENTS
    --------------------------------------------------------- */

    statusTabs.forEach(tab => {

        tab.addEventListener(
            "click",
            function () {

                showStatusPanel(
                    this.dataset.statusTab
                );

            }
        );

    });


    /* ---------------------------------------------------------
       DEFAULT VIEW
       Upcoming Classes
    --------------------------------------------------------- */

    showStatusPanel("upcoming");

});