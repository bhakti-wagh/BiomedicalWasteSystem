async function loadAlerts() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/alerts"
        );

        const alerts = await response.json();

        const tableBody =
            document.getElementById("alertTableBody");

        tableBody.innerHTML = "";


        if (alerts.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td colspan="7">
                        No alerts found.
                    </td>
                </tr>
            `;

            return;
        }


        alerts.forEach(function(alert) {

            const row = document.createElement("tr");


            let action = "";


            if (alert.status === "OPEN") {

                action = `
                    <button onclick="resolveAlert(${alert.alert_id})">
                        Resolve
                    </button>
                `;

            } else {

                action = "Resolved";

            }


            row.innerHTML = `

                <td>${alert.alert_id}</td>

                <td>${alert.bin_id || "-"}</td>

                <td>${alert.alert_type}</td>

                <td>${alert.message}</td>

                <td>${alert.severity}</td>

                <td>${alert.status}</td>

                <td>${action}</td>

            `;


            tableBody.appendChild(row);

        });

    } catch (error) {

        console.error("Alert loading error:", error);

        document.getElementById("alertTableBody").innerHTML = `
            <tr>
                <td colspan="7">
                    Unable to load alerts.
                </td>
            </tr>
        `;

    }

}


// Resolve Alert

async function resolveAlert(alertId) {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/alerts/" + alertId,
            {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: "RESOLVED"
                })

            }
        );


        const data = await response.json();


        if (response.ok) {

            alert("Alert resolved successfully.");

            loadAlerts();

        } else {

            alert(data.message);

        }

    } catch (error) {

        console.error(error);

        alert("Unable to connect to server.");

    }

}


// Logout

document.getElementById("logoutBtn")
.addEventListener("click", function() {

    localStorage.removeItem("user");

    window.location.href = "first.html";

});


loadAlerts();