    document
        .querySelectorAll(".training-attendance-bar-fill")
        .forEach((bar) => {

            const percentage =
                parseFloat(bar.dataset.percentage) || 0;

            bar.style.width =
                `${Math.min(Math.max(percentage, 0), 100)}%`;
        });
