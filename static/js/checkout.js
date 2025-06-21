document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("checkout-form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            console.log(value);
            console.log(key);
            data[key] = value;
        });

        fetch("https://alsouraya.onrender.com/finalize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                alert("Order placed successfully!");
                window.location.href = "/products-page";
            } else {
                return response.json().then(errorData => {
                    alert(errorData.error);  // Display the actual message like "Invalid phone number"
                });
            }
        })
        .catch(() => alert("Network error. Try again."));
    });
});
