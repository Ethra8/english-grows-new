const toggleButton = document.getElementById("mobileSidebarToggle");
const sidebar = document.getElementById("profileSidebar");
const backdrop = document.getElementById("sidebarBackdrop");

if (toggleButton && sidebar && backdrop) {
    const openSidebar = () => {
        sidebar.classList.add("sidebar-open");
        backdrop.classList.add("backdrop-open");
        document.body.classList.add("mobile-sidebar-active");

        toggleButton.setAttribute("aria-expanded", "true");
        toggleButton.setAttribute("aria-label", "Close navigation menu");
    };

    const closeSidebar = () => {
        sidebar.classList.remove("sidebar-open");
        backdrop.classList.remove("backdrop-open");
        document.body.classList.remove("mobile-sidebar-active");

        toggleButton.setAttribute("aria-expanded", "false");
        toggleButton.setAttribute("aria-label", "Open navigation menu");
    };

    toggleButton.addEventListener("click", () => {
        const isOpen = sidebar.classList.contains("sidebar-open");

        if (isOpen) {
            closeSidebar();
        } else {
            openSidebar();
        }
    });

    backdrop.addEventListener("click", closeSidebar);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });

    sidebar.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            if (window.innerWidth < 992) {
                closeSidebar();
            }
        });
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth >= 992) {
            closeSidebar();
        }
    });
}