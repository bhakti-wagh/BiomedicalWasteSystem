async function loadBins() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/bins"
        );

        const bins = await response.json();

        const tableBody = document.getElementById("binTableBody");

        tableBody.innerHTML = "";


        bins.forEach(function(bin) {

            const row = document.createElement("tr");

            const capacityPercentage =
                (bin.current_level / bin.max_capacity) * 100;


            row.innerHTML = `

                <td>${bin.bin_id}</td>

                <td>${bin.location_id}</td>

                <td>${bin.category_id}</td>

                <td>${bin.bin_type}</td>

                <td>${bin.max_capacity} kg</td>

                <td>${bin.current_level} kg</td>

                <td>${bin.status}</td>

                <td>${capacityPercentage.toFixed(1)}%</td>

            `;


            tableBody.appendChild(row);

        });

    } catch (error) {

        console.error("Bin loading error:", error);

        document.getElementById("binTableBody").innerHTML = `
            <tr>
                <td colspan="8">
                    Unable to load bins.
                </td>
            </tr>
        `;

    }

}


loadBins();


// Logout

document.getElementById("logoutBtn").addEventListener("click", function() {

    localStorage.removeItem("user");

    window.location.href = "first.html";

});