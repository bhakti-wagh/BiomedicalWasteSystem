const binSelect = document.getElementById("bin");


// Load Bins

async function loadBins() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/bins"
        );

        const bins = await response.json();

        bins.forEach(function(bin) {

            const option = document.createElement("option");

            option.value = bin.bin_id;

            option.textContent =
                "Bin " + bin.bin_id +
                " - " + bin.current_level +
                "/" + bin.max_capacity + " kg";

            binSelect.appendChild(option);

        });

    } catch (error) {

        console.error("Bin loading error:", error);

    }

}


// Load Collections

async function loadCollections() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/collections"
        );

        const collections = await response.json();

        const tableBody =
            document.getElementById("collectionTableBody");

        tableBody.innerHTML = "";


        collections.forEach(function(collection) {

            const row = document.createElement("tr");

            row.innerHTML = `

                <td>${collection.collection_id}</td>

                <td>${collection.waste_record_id}</td>

                <td>${collection.bin_id}</td>

                <td>${collection.collected_by}</td>

                <td>${collection.quantity_collected} kg</td>

                <td>${collection.status}</td>

            `;

            tableBody.appendChild(row);

        });

    } catch (error) {

        console.error("Collection loading error:", error);

    }

}


// Complete Collection

document.getElementById("collectionForm")
.addEventListener("submit", async function(event) {

    event.preventDefault();


    const wasteRecordId =
        document.getElementById("wasteRecord").value;

    const binId =
        document.getElementById("bin").value;

    const quantity =
        document.getElementById("quantity").value;


    const user =
        JSON.parse(localStorage.getItem("user"));


    if (!user) {

        document.getElementById("message").textContent =
            "Please login first.";

        return;

    }


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/collections",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    waste_record_id: wasteRecordId,

                    bin_id: binId,

                    collected_by: user.user_id,

                    quantity_collected: quantity

                })

            }
        );


        const data = await response.json();


        if (response.ok) {

            document.getElementById("message").textContent =
                "Collection completed successfully. " +
                "Collection ID: " +
                data.collection_id +
                ". Bin " +
                data.bin_id +
                " is now at " +
                data.new_level +
                " kg.";

            document.getElementById("collectionForm").reset();

            loadBins();

            loadCollections();

        } else {

            document.getElementById("message").textContent =
                data.message;

        }

    } catch (error) {

        console.error(error);

        document.getElementById("message").textContent =
            "Unable to connect to server.";

    }

});


// Logout

document.getElementById("logoutBtn")
.addEventListener("click", function() {

    localStorage.removeItem("user");

    window.location.href = "first.html";

});


loadBins();
loadCollections();