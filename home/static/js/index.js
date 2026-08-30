// =======================================================
//     PLATFORM SLIDESHOW
// =======================================================

document.addEventListener("DOMContentLoaded", function () {
    const laptop = document.getElementById("platform-laptop");
    const slides = Array.from(
        document.querySelectorAll(".platform-slide")
    );
    const dots = Array.from(
        document.querySelectorAll(".platform-slide-dot")
    );
    const currentSlideLabel = document.getElementById(
        "platform-current-slide"
    );
    const liveDescription = document.getElementById(
        "platform-slide-description"
    );

    const slideIntervalTime = 4500;
    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    let currentSlideIndex = 0;
    let slideInterval = null;


    function displaySlide(index) {
        if (!slides.length) {
            return;
        }

        currentSlideIndex = index;

        slides.forEach(function (slide, slideIndex) {
            const isActive = slideIndex === currentSlideIndex;

            slide.classList.toggle("active", isActive);
            slide.setAttribute(
                "aria-hidden",
                isActive ? "false" : "true"
            );
        });

        dots.forEach(function (dot, dotIndex) {
            const isActive = dotIndex === currentSlideIndex;

            dot.classList.toggle("active", isActive);
            dot.setAttribute(
                "aria-pressed",
                isActive ? "true" : "false"
            );
        });

        const activeSlide = slides[currentSlideIndex];

        const isPersonSlide = activeSlide.classList.contains(
            "platform-slide-person"
        );

        if (laptop) {
            laptop.classList.toggle(
                "person-slide-active",
                isPersonSlide
            );
        }

        const slideTitle =
            activeSlide.dataset.slideTitle || "Platform preview";

        if (currentSlideLabel) {
            currentSlideLabel.textContent = slideTitle;
        }

        if (liveDescription) {
            liveDescription.textContent = slideTitle;
        }
    }


    function showNextSlide() {
        const nextSlideIndex =
            (currentSlideIndex + 1) % slides.length;

        displaySlide(nextSlideIndex);
    }


    function startSlideshow() {
        if (
            prefersReducedMotion ||
            slides.length < 2 ||
            slideInterval
        ) {
            return;
        }

        slideInterval = window.setInterval(
            showNextSlide,
            slideIntervalTime
        );
    }


    function stopSlideshow() {
        if (!slideInterval) {
            return;
        }

        window.clearInterval(slideInterval);
        slideInterval = null;
    }


    dots.forEach(function (dot) {
        dot.addEventListener("click", function () {
            const selectedIndex = Number(
                dot.dataset.slideIndex
            );

            stopSlideshow();
            displaySlide(selectedIndex);
            startSlideshow();
        });
    });


    if (laptop) {
        laptop.addEventListener("mouseenter", stopSlideshow);
        laptop.addEventListener("mouseleave", startSlideshow);

        laptop.addEventListener("focusin", stopSlideshow);
        laptop.addEventListener("focusout", startSlideshow);
    }


    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            stopSlideshow();
        } else {
            startSlideshow();
        }
    });


    displaySlide(0);
    startSlideshow();
});
