document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            username: form.username.value,
            password: form.password.value
        };

        try {
            const response = await fetch("https://alsouraya.onrender.com/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                alert("Signup successful!");
                window.location.href = "/products-page";
            } else {
                const errorText = await response.text();
                alert("Signup failed: " + errorText);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred.");
        }
    });
});
