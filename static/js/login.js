document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            username: form.username.value,
            password: form.password.value
        };

        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                if (response.redirected) {
                    window.location.href = response.url;
                }
                else{
                    window.location.href = "/products-page"; // change to your target route
                }
            } else {
                alert("Login failed");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});
