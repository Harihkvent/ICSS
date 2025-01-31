document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    if (registerForm) {
        registerForm.addEventListener("submit", (event) => {
            event.preventDefault();
            localStorage.setItem("userEmail", document.getElementById("registerEmail").value);
            localStorage.setItem("userPassword", document.getElementById("registerPassword").value);
            alert("Registration Successful!");
            window.location.href = "home.html";
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;
            
            if (email === localStorage.getItem("userEmail") && password === localStorage.getItem("userPassword")) {
                localStorage.setItem("loggedInUser", email);
                window.location.href = "home.html";
            } else {
                alert("Invalid login credentials!");
            }
        });
    }
});
