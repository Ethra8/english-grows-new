(() => {
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll("#changelist-filter details").forEach(filter => {
            filter.removeAttribute("open");
        });
    });
})();