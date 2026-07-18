console.log("FactoryFlow Loaded Successfully");

// ===========================
// Revenue Bar Chart
// ===========================

const revenueCtx = document.getElementById("revenueChart");

if (revenueCtx) {

    new Chart(revenueCtx, {
        type: "bar",

        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],

            datasets: [
                {
                    label: "Income",
                    data: [90000, 120000, 100000, 150000, 130000, 125000],
                    backgroundColor: "#2563eb",
                    borderRadius: 8
                },
                {
                    label: "Expenses",
                    data: [60000, 75000, 70000, 80000, 76000, 78500],
                    backgroundColor: "#ef4444",
                    borderRadius: 8
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

}


// =====================================
// ADD THE PIE CHART CODE BELOW HERE
// =====================================

const expenseCtx = document.getElementById("expenseChart");

if (expenseCtx) {

    new Chart(expenseCtx, {

        type: "pie",

        data: {

            labels: [
                "Raw Materials",
                "Salaries",
                "Electricity",
                "Transport",
                "Maintenance",
                "Others"
            ],

            datasets: [{

                data: [45,20,10,10,10,5],

                backgroundColor: [
                    "#2563eb",
                    "#22c55e",
                    "#f59e0b",
                    "#8b5cf6",
                    "#ef4444",
                    "#9ca3af"
                ],

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,
            maintainAspectRatio: false,

            plugins: {

                legend: {
                    position: "right"
                }

            }

        }

    });

}