// ============================
// SWITCH TABS
// ============================
function showTab(event, tabId) {
    document.querySelectorAll(".tab-content").forEach(tab => {
        tab.classList.remove("active");
    });

    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    document.getElementById(tabId).classList.add("active");
    event.target.classList.add("active");
}

// ============================
// MODAL UPDATE
// ============================
function openUpdateModal(id, statut, description, descriptionAdmin) {
    document.getElementById("incidentId").value = id;
    document.getElementById("newStatut").value = statut;
    document.getElementById("descriptionClient").value = description || '';
    document.getElementById("descriptionAdmin").value = descriptionAdmin || '';

    document.getElementById("updateModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("updateModal").style.display = "none";
}

function updateStatut() {
    const id = document.getElementById("incidentId").value;
    const statut = document.getElementById("newStatut").value;
    const descriptionAdmin = document.getElementById("descriptionAdmin").value;

    fetch(`/incidents/${id}/statut`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            statut: statut,
            description_admin: descriptionAdmin
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erreur serveur");
        }
        location.reload();
    })
    .catch(error => {
        console.error("Erreur:", error);
        alert("Erreur lors de la mise à jour");
    });
}

// button refersh
function refreshInterventions() {

    const button = document.querySelector(".btn-refresh");

    // Animation rotation
    button.style.transform = "rotate(360deg)";

    fetch("/dashboard?refresh=1")
        .then(response => window.location.reload());
}