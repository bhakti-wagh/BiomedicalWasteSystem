const categorySelect = document.getElementById("category");
const locationSelect = document.getElementById("location");


// Load Categories

async function loadCategories() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/categories"
        );

        const categories = await response.json();

        categories.forEach(function(category) {

            const option = document.createElement("option");

            option.value = category.category_id;
            option.textContent = category.name;

            categorySelect.appendChild(option);

        });

    } catch (error) {

        console.error("Category loading error:", error);

    }
}


// Load Locations

async function loadLocations() {

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/locations"
        );

        const locations = await response.json();

        locations.forEach(function(location) {

            const option = document.createElement("option");

            option.value = location.location_id;
            option.textContent = location.name;

            locationSelect.appendChild(option);

        });

    } catch (error) {

        console.error("Location loading error:", error);

    }
}


// Load data when page opens

loadCategories();
loadLocations();



document.getElementById("wasteForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const wasteType = document.getElementById("wasteType").value;
    const categoryId = document.getElementById("category").value;
    const locationId = document.getElementById("location").value;
    const quantity = document.getElementById("quantity").value;

    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
        document.getElementById("message").textContent =
            "Please login first.";
        return;
    }

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/api/waste-records",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    category_id: categoryId,
                    location_id: locationId,
                    created_by: user.user_id,
                    waste_type: wasteType,
                    quantity: quantity
                })
            }
        );

        const data = await response.json();

        if (response.ok) {

    const binResponse = await fetch(
        "http://127.0.0.1:5000/api/assign-bin",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                location_id: locationId,
                category_id: categoryId,
                quantity: quantity
            })
        }
    );

    const binData = await binResponse.json();

   if (binResponse.ok) {

    const updateBinResponse = await fetch(
        "http://127.0.0.1:5000/api/update-bin-level",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                bin_id: binData.bin_id,
                quantity: quantity
            })
        }
    );

    const updateBinData = await updateBinResponse.json();

    if (updateBinResponse.ok) {

        document.getElementById("message").textContent =
            "Waste recorded successfully. " +
            "Record ID: " + data.waste_record_id +
            ". Bin " + binData.bin_id +
            " updated successfully.";

    } else {

        document.getElementById("message").textContent =
            "Waste recorded and bin found, but bin level could not be updated.";
    }

}

    document.getElementById("wasteForm").reset();

}

    } catch (error) {

        console.error(error);

        document.getElementById("message").textContent =
            "Unable to connect to server.";
    }

});