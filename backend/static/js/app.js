console.log("FactoryFlow Loaded Successfully");

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