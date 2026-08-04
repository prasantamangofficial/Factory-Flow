console.log("FactoryFlow Loaded Successfully");
// Chart.js draws onto a canvas, so CSS can't reach its text or gridlines.
// Read the theme and set them explicitly.
function applyChartTheme() {
    const dark = document.documentElement.getAttribute("data-theme") === "dark";
    Chart.defaults.color = dark ? "#94A3B8" : "#666";
    Chart.defaults.borderColor = dark ? "#243044" : "#e5e7eb";
}
applyChartTheme();
const PIE_COLORS = [
    "#2563eb", "#22c55e", "#f59e0b",
    "#8b5cf6", "#ef4444", "#9ca3af",
    "#06b6d4", "#ec4899"
];

function money(n) {
    return "NPR " + Number(n).toLocaleString();
}

function drawRevenueChart(data) {
    const el = document.getElementById("revenueChart");
    if (!el) return;

    new Chart(el, {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Income",
                    data: data.income,
                    backgroundColor: "#2563eb",
                    borderRadius: 8
                },
                {
                    label: "Expenses",
                    data: data.expenses,
                    backgroundColor: "#ef4444",
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                tooltip: {
                    callbacks: {
                        label: c => c.dataset.label + ": " + money(c.parsed.y)
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: v => Number(v).toLocaleString() }
                }
            }
        }
    });
}

function drawExpenseChart(breakdown) {
    const el = document.getElementById("expenseChart");
    if (!el) return;

    const legend = document.getElementById("pieLegend");

    if (!breakdown.labels.length) {
        if (legend) {
            legend.innerHTML = "<p style='color:#94a3b8'>No expenses this month.</p>";
        }
        return;
    }

    new Chart(el, {
        type: "pie",
        data: {
            labels: breakdown.labels,
            datasets: [{
                data: breakdown.values,
                backgroundColor: PIE_COLORS,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 1,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: c => c.label + ": " + money(c.parsed)
                    }
                }
            }
        }
    });

    if (legend) {
        const total = breakdown.values.reduce((a, b) => a + b, 0);

        legend.innerHTML = breakdown.labels.map((label, i) => {
            const pct = total ? Math.round((breakdown.values[i] / total) * 100) : 0;
            return `
                <div class="legend-item">
                    <span class="legend-color" style="background:${PIE_COLORS[i % PIE_COLORS.length]}"></span>
                    <span>${label}</span>
                    <strong>${pct}%</strong>
                </div>`;
        }).join("");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (!document.getElementById("revenueChart")) return;

    fetch("/api/dashboard-charts/")
        .then(r => r.json())
        .then(data => {
            drawRevenueChart(data);
            drawExpenseChart(data.breakdown);
        })
        .catch(err => console.error("Chart data failed:", err));
});

/* THEME TOGGLE*/

(function () {
    const STORAGE_KEY = "factoryflow-theme";

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);

        const icon = document.querySelector("#themeToggle i");
        if (icon) {
            icon.className = theme === "dark"
                ? "fa-solid fa-sun"
                : "fa-solid fa-moon";
        }
    }

    // Saved choice wins; otherwise follow the operating system.
    const saved = localStorage.getItem(STORAGE_KEY);
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(saved || (prefersDark ? "dark" : "light"));

    document.addEventListener("DOMContentLoaded", () => {
        const btn = document.getElementById("themeToggle");
        if (!btn) return;

        // Re-apply now that the icon element exists.
        applyTheme(document.documentElement.getAttribute("data-theme"));

        btn.addEventListener("click", () => {
            const next = document.documentElement.getAttribute("data-theme") === "dark"
                ? "light"
                : "dark";
            applyTheme(next);
            localStorage.setItem(STORAGE_KEY, next);
        });
    });
})();
