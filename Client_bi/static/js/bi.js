document.addEventListener("DOMContentLoaded", () => {
    loadTotals();
    loadIncidentsByType();
    loadAbsencesByType();
    loadAbsencesByType_bar();
});

/* =========================
   KPI TOTALS
========================= */
async function loadTotals() {
    try {
        const incRes = await fetch("http://127.0.0.1:5200/stats/incidents/total");
        const incData = await incRes.json();
        document.getElementById("kpi-incidents").innerText = incData.total;

        const absRes = await fetch("http://127.0.0.1:5200/stats/absences/total");
        const absData = await absRes.json();
        document.getElementById("kpi-absences").innerText = absData.total;

    } catch (err) {
        console.error("Erreur KPI :", err);
    }
}

/* =========================
   INCIDENTS PAR TYPE (radar)
========================= */
let incidentsChart = null;

async function loadIncidentsByType() {
    try {
        const res = await fetch("http://127.0.0.1:5200/stats/incidents/by-type");
        const data = await res.json();

        const ctx = document.getElementById("incidentsChart").getContext("2d");

        if (incidentsChart) {
            incidentsChart.destroy();
        }

        incidentsChart = new Chart(ctx, {
            type: "bar",    /* type de graphe  */
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Incidents",
                    data: data.values,
                    backgroundColor: "#2563eb"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                }
            }
        });

    } catch (err) {
        console.error("Erreur incidents chart :", err);
    }
}

/* =========================
   ABSENCES PAR TYPE (doughnut)
========================= */
let absencesChart = null;

async function loadAbsencesByType() {
    try {
        const res = await fetch("http://127.0.0.1:5200/stats/absences/by-type");
        const data = await res.json();

        const ctx = document.getElementById("absencesChart").getContext("2d");

        if (absencesChart) {
            absencesChart.destroy();
        }

        absencesChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        "#2563eb",
                        "#f59e0b",
                        "#10b981",
                        "#ef4444",
                        "#8b5cf6"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });

    } catch (err) {
        console.error("Erreur absences chart :", err);
    }
}


/* =========================
   ABSENCES PAR TYPE (bar)
========================= */
let absencesChart_bar = null;

async function loadAbsencesByType_bar() {
    try {
        const res = await fetch("http://127.0.0.1:5200/stats/absences/by-type");
        const data = await res.json();

        const ctx = document.getElementById("absencesChart_bar").getContext("2d");

        if (absencesChart_bar) {
            absencesChart_bar.destroy();
        }

        absencesChart_bar = new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        "#2563eb",
                        "#f59e0b",
                        "#10b981",
                        "#ef4444",
                        "#8b5cf6"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" }
                }
            }
        });

    } catch (err) {
        console.error("Erreur absences chart :", err);
    }
}

/* =========================
   STAT SERVICE FAIT
========================= */

async function loadServiceFaitBI() {

    const response = await fetch("http://127.0.0.1:5200/stats/servicefait");
    const data = await response.json();

    // KPI
    document.getElementById("kpi-interventions").innerText = data.total_interventions;
    document.getElementById("kpi-revenue").innerText =
        data.total_revenue.toFixed(2) + " $";

    // Graph interventions par jour
    const labels = Object.keys(data.interventions_by_date);
    const values = Object.values(data.interventions_by_date);

    new Chart(document.getElementById("interventionsChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Interventions par jour",
                data: values,
                borderColor: "#1e5bb8",
                fill: false
            }]
        }
    });
}

loadServiceFaitBI();