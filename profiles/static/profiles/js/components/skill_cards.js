document.addEventListener("DOMContentLoaded", function () {

    const accordionToggles = document.querySelectorAll(".skill-accordion-toggle");

    accordionToggles.forEach(function (toggle) {

        toggle.addEventListener("click", function () {

            const body = document.getElementById(toggle.getAttribute("aria-controls"));

            if (!body) return;

            const isOpen = toggle.getAttribute("aria-expanded") === "true";

            toggle.setAttribute("aria-expanded", isOpen ? "false" : "true");

            body.hidden = isOpen;

        });

    });

});
