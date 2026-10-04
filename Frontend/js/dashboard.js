
const user = JSON.parse(localStorage.getItem("user"));

console.log(user);

document.getElementById("userName").textContent = user.name;
document.getElementById("userRole").textContent = user.role;

async function loadDashboard() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/dashboard"
        );

        const data = await response.json();

        document.getElementById("totalWaste").textContent =
            data.total_waste + " kg";

        document.getElementById("totalBins").textContent =
            data.total_bins;

        document.getElementById("nearFullBins").textContent =
            data.near_full_bins;

        document.getElementById("openAlerts").textContent =
            data.open_alerts;

        document.getElementById("totalCollections").textContent =
            data.total_collections;

    } catch (error) {

        console.error("Dashboard error:", error);

    }
}

loadDashboard();


document.getElementById("logoutBtn").addEventListener("click", function() {

    localStorage.removeItem("user");

    window.location.href = "first.html";

});