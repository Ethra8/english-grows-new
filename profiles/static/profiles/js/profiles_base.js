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

