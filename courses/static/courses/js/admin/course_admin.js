document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#course_form");
    if (!form) return;

    let submitted = false;

    form.addEventListener("submit", event => {
        if (submitted) {
            event.preventDefault();
            return;
        }

        submitted = true;

        form.querySelectorAll(
            'input[type="submit"], button[type="submit"]'
        ).forEach(button => {
            button.disabled = true;
        });
    });
});