// =========================================================
// INDIVIDUAL SKILLS PROGRESS GRAPH
// 4 skill lines: Speaking, Listening, Reading, Writing
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const chartEl = document.getElementById("skillsProgressChart");
    const chartDataEl = document.getElementById("skills-chart-data");

    // This JS file may be loaded on pages where this chart
    // does not exist. In that case, do nothing.
    if (!chartEl || !chartDataEl) {
        return;
    }


    // ---------------------------------------------------------
    // GET CHART DATA
    //
    // Empty data is VALID:
    //
    // {
    //     "labels": [],
    //     "datasets": []
    // }
    //
    // Chart.js will still render the chart and Y axis.
    // ---------------------------------------------------------

    const chartData = JSON.parse(
        chartDataEl.textContent
    );

    console.log(
        "Student chart data:",
        chartData
    );


    // ---------------------------------------------------------
    // CUSTOM PLUGIN:
    // SEPARATE OVERLAPPING SKILL DOTS
    //
    // If two or more skills have the exact same score
    // on the same date, their points would normally overlap.
    //
    // This plugin keeps the REAL data coordinates unchanged,
    // but visually offsets the dots a few pixels horizontally
    // so every skill colour remains visible.
    //
    // If there are no datasets yet, this simply has
    // nothing to draw.
    // ---------------------------------------------------------

    const separateOverlappingPoints = {
        id: "separateOverlappingPoints",

        afterDatasetsDraw(chart) {

            const { ctx } = chart;
            const groups = new Map();


            // -------------------------------------------------
            // FIND POINTS THAT SHARE THE SAME X + Y POSITION
            // -------------------------------------------------

            chart.data.datasets.forEach(function (
                dataset,
                datasetIndex
            ) {

                const meta = chart.getDatasetMeta(
                    datasetIndex
                );

                if (meta.hidden) {
                    return;
                }

                meta.data.forEach(function (
                    point,
                    pointIndex
                ) {

                    const rawValue = (
                        dataset.data[pointIndex]
                    );

                    if (
                        rawValue === null
                        || rawValue === undefined
                    ) {
                        return;
                    }


                    // Round pixel coordinates slightly so tiny
                    // floating-point differences do not prevent
                    // genuinely overlapping points being grouped.

                    const key = (
                        Math.round(point.x)
                        + "-"
                        + Math.round(point.y)
                    );


                    if (!groups.has(key)) {
                        groups.set(key, []);
                    }


                    groups.get(key).push({
                        dataset: dataset,
                        point: point
                    });
                });
            });


            // -------------------------------------------------
            // DRAW POINTS
            // -------------------------------------------------

            groups.forEach(function (points) {

                // ---------------------------------------------
                // ONE POINT:
                // Draw normally at its real position.
                // ---------------------------------------------

                if (points.length === 1) {

                    drawPoint(
                        ctx,
                        points[0].point.x,
                        points[0].point.y,
                        points[0].dataset.backgroundColor
                    );

                    return;
                }


                // ---------------------------------------------
                // MULTIPLE OVERLAPPING POINTS:
                //
                // Move them slightly left/right around the
                // REAL X position.
                //
                // Example:
                //
                //      ●  ●
                //
                // instead of:
                //
                //       ●
                // ---------------------------------------------

                const spacing = 8;

                const totalWidth = (
                    (points.length - 1)
                    * spacing
                );

                const startOffset = (
                    -(totalWidth / 2)
                );


                points.forEach(function (
                    item,
                    index
                ) {

                    const offsetX = (
                        startOffset
                        + (index * spacing)
                    );


                    drawPoint(
                        ctx,
                        item.point.x + offsetX,
                        item.point.y,
                        item.dataset.backgroundColor
                    );
                });
            });
        }
    };


    // ---------------------------------------------------------
    // DRAW CUSTOM POINT
    // ---------------------------------------------------------

    function drawPoint(ctx, x, y, color) {

        ctx.save();

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            5,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = color;
        ctx.fill();

        // White outline helps overlapping colours remain
        // visually distinct.

        ctx.lineWidth = 1.5;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();

        ctx.restore();
    }


    // ---------------------------------------------------------
    // APPLY CONSISTENT VISUAL SETTINGS
    //
    // With datasets: normal styling is applied.
    // Without datasets: forEach simply has nothing to process.
    // ---------------------------------------------------------

    chartData.datasets.forEach(function (dataset) {

        dataset.tension = 0.2;
        dataset.fill = false;
        dataset.borderWidth = 2.5;

        // Hide Chart.js default points because our plugin
        // redraws them and handles overlapping values.

        dataset.pointRadius = 0;

        // Still keep a generous hover/click area around
        // the REAL data coordinate.

        dataset.pointHitRadius = 12;
        dataset.pointHoverRadius = 0;
    });


    // ---------------------------------------------------------
    // CREATE CHART
    //
    // IMPORTANT:
    // The chart is created EVEN WHEN labels/datasets are empty.
    // This keeps the graph structure visible before the
    // learner's first assessment.
    // ---------------------------------------------------------

    new Chart(chartEl, {

        type: "line",

        data: chartData,

        // Register our custom point plugin.

        plugins: [
            separateOverlappingPoints
        ],

        options: {

            responsive: true,
            maintainAspectRatio: false,
            spanGaps: true,

            interaction: {
                mode: "index",
                intersect: false
            },

            scales: {

                y: {
                    min: 0,
                    max: 10,

                    ticks: {
                        stepSize: 1,

                        callback: function (value) {
                            return value;
                        }
                    },

                    title: {
                        display: true,
                        text: "Assessment score / 10"
                    }
                },

                x: {
                    title: {
                        display: false
                    }
                }
            },

            plugins: {

                legend: {
                    position: "bottom",

                    labels: {
                        usePointStyle: true,
                        pointStyle: "circle",
                        padding: 18
                    }
                },

                tooltip: {
                    callbacks: {

                        label: function (context) {

                            const value = (
                                context.parsed.y
                            );

                            return (
                                context.dataset.label
                                + ": "
                                + Number(value)
                                    .toFixed(1)
                                    .replace(".0", "")
                                + " / 10"
                            );
                        }
                    }
                }
            }
        }
    });
});





// =========================================================
// OVERALL SKILLS PROGRESS GRAPH
// 1 DOT / LINE = average of the 4 skills
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const chartEl = document.getElementById(
        "overallSkillsProgressChart"
    );

    const chartDataEl = document.getElementById(
        "overall-skills-chart-data"
    );


    // This JS file may be loaded on pages where this chart
    // does not exist. In that case, do nothing.

    if (!chartEl || !chartDataEl) {
        return;
    }


    // ---------------------------------------------------------
    // GET CHART DATA
    //
    // Empty data is VALID and should still create the graph.
    // ---------------------------------------------------------

    const chartData = JSON.parse(
        chartDataEl.textContent
    );


    console.log(
        "Overall skills chart data:",
        chartData
    );


    // ---------------------------------------------------------
    // APPLY DATASET SETTINGS
    //
    // If no assessment data exists yet, datasets is empty,
    // so nothing happens here and the chart still renders.
    // ---------------------------------------------------------

    chartData.datasets.forEach(function (dataset) {

        dataset.tension = 0.2;
        dataset.fill = false;
        dataset.borderWidth = 2.5;
        dataset.pointRadius = 5;
        dataset.pointHoverRadius = 7;
    });


    // ---------------------------------------------------------
    // CREATE CHART
    //
    // IMPORTANT:
    // Do NOT return when labels is empty.
    //
    // The empty chart is intentional and represents the
    // learner's pre-assessment state.
    // ---------------------------------------------------------

    new Chart(chartEl, {

        type: "line",

        data: chartData,

        options: {

            responsive: true,
            maintainAspectRatio: false,
            spanGaps: true,

            scales: {

                y: {
                    min: 0,
                    max: 10,

                    ticks: {
                        stepSize: 1
                    },

                    title: {
                        display: true,
                        text: "Overall assessment / 10"
                    }
                },

                x: {
                    title: {
                        display: false
                    }
                }
            },

            plugins: {

                legend: {
                    display: false
                },

                tooltip: {
                    callbacks: {

                        label: function (context) {

                            const value = Number(
                                context.parsed.y
                            )
                            .toFixed(1)
                            .replace(".0", "");

                            return (
                                "Overall skills: "
                                + value
                                + " / 10"
                            );
                        }
                    }
                }
            }
        }
    });
});