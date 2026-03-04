
// Affiche panale Les données ont été enregistrées et envoyées avec succès
function handleFormSubmission(e) {
    // 1. On empêche l'envoi immédiat pour montrer le message
    e.preventDefault();
    const form = e.target;

    // 2. Création et affichage de la notification
    const notification = document.createElement("div");
    notification.className = "success-notification";
    notification.innerHTML = `
        <div class="notification-content">
            <span class="icon">🛡️</span>
            <div class="text-group">
                <strong>Transmission réussie</strong>
                <p>Les données ont été enregistrées et envoyées avec succès.</p>
            </div>
        </div>
    `;
    document.body.appendChild(notification);

    // 3. On attend 2 secondes pour que l'utilisateur voie le message, puis on envoie
    setTimeout(() => {
        notification.classList.add("fade-out");

        setTimeout(() => {
            // 4. L'envoi RÉEL des données au serveur
            form.submit();
            clearForm(form);
        }, 500);
    }, 2000);
}

// Application aux deux formulaires
const form1 = document.getElementById("Form");
if (form1) {
    form1.addEventListener("submit", handleFormSubmission);
}

const form2 = document.getElementById("Form2");
if (form2) {
    form2.addEventListener("submit", handleFormSubmission);
}

function showTab(tabId) {

    // cacher tous les contenus
    document.querySelectorAll(".tab-content").forEach(tab => {
        tab.classList.remove("active");
    });

    // désactiver tous les boutons
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.remove("active");
    });

    // activer le bon contenu
    document.getElementById(tabId).classList.add("active");

    // activer le bouton cliqué
    const buttons = document.querySelectorAll(".tab-btn");
    buttons.forEach(btn => {
        if (btn.textContent.toLowerCase().includes(tabId)) {
            btn.classList.add("active");
        }
    });
}

// Login Script :

    // Toggle afficher / masquer mot de passe
    const togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function () {
            const passwordInput = document.getElementById('password');
            const icon = this.querySelector('i');

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }

    // Validation du formulaire login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('errorMessage');

            if (username === '' || password === '') {
                errorMessage.textContent = 'Veuillez remplir tous les champs';
                errorMessage.classList.add('active');
                return;
            }

            // Simulation (à remplacer par backend Flask)
            if (username === 'admin' && password === 'admin123') {
                errorMessage.classList.remove('active');
                window.location.href = '/dashboard';
            } else {
                errorMessage.textContent = 'Identifiant ou mot de passe incorrect';
                errorMessage.classList.add('active');
            }
        });
    }

    // Effacer message d'erreur quand l'utilisateur tape
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    if (usernameInput) {
        usernameInput.addEventListener('input', function () {
            document.getElementById('errorMessage').classList.remove('active');
        });
    }

    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            document.getElementById('errorMessage').classList.remove('active');
        });
    }

//FIN script login

//script clean all champs apres validation or annulation

function clearForm(form) {
    form.querySelectorAll('input, textarea, select').forEach(field => {
        field.value = '';
    });
}

document.querySelectorAll('.annuler').forEach(btn => {
    btn.addEventListener('click', function () {
        const form = this.closest('form');
        if (form) clearForm(form);
    });
});

