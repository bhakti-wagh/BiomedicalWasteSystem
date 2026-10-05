// Load Dashboard Summary

async function loadSummary() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/dashboard"
        );

        const data = await response.json();


        document.getElementById("totalWaste").textContent =
            data.total_waste + " kg";

        document.getElementById("totalBins").textContent =
            data.total_bins;

        document.getElementById("totalCollections").textContent =
            data.total_collections;

        document.getElementById("openAlerts").textContent =
            data.open_alerts;

    } catch (error) {

        console.error("Summary loading error:", error);

    }

}


// Load Waste Records

async function loadWasteRecords() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/waste-records"
        );

        const records = await response.json();

        const tableBody =
            document.getElementById("wasteTableBody");

        tableBody.innerHTML = "";


        records.forEach(function(record) {

            const row = document.createElement("tr");

            row.innerHTML = `

                <td>${record.waste_record_id}</td>

                <td>${record.waste_type}</td>

                <td>${record.category_id}</td>

                <td>${record.location_id}</td>

                <td>${record.quantity} kg</td>

                <td>${record.record_date}</td>

                <td>${record.status}</td>

            `;

            tableBody.appendChild(row);

        });

    } catch (error) {

        console.error("Waste record loading error:", error);

    }

}


// Logout

document.getElementById("logoutBtn")
.addEventListener("click", function() {

    localStorage.removeItem("user");

    window.location.href = "first.html";

});


loadSummary();
loadWasteRecords();