// Responsiveness for maintenance banner height
document.addEventListener("DOMContentLoaded", () => {
    const banner = document.querySelector(".maintenance-banner");
    if (!banner) {
        console.warn("Maintenance banner not found.");
        return;
    }

    const updateBannerHeight = () => {
        const height = banner.getBoundingClientRect().height;
        document.documentElement.style.setProperty("--maintenance-banner-height", `${height}px`);
        console.log("Maintenance banner height:", height);
    };

    updateBannerHeight();
    const observer = new ResizeObserver(updateBannerHeight);
    observer.observe(banner);
});