const insert_inventory = async () => {
    const data = {
        item_name: document.getElementById("item_name").value,
        description: document.getElementById("description").value,
        category: document.getElementById("category").value,
        uom: document.getElementById("uom").value,
        supplier: document.getElementById("supplier").value,
        price: document.getElementById("price").value,
        quantity_in_stock: document.getElementById("quantity_in_stock").value,
        minimum_stock_level: document.getElementById("minimum_stock_level").value,
    };

    try {
        const response = await fetch(`/api-insert-inventory-rizal-employee/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();

       
        if (response.status === 401) {
            window.alert("Unauthorized credential. Please login");
        } else if (responseData.error) {
            window.alert("Error: " + responseData.error);
        } else if (response.status === 200) {
            window.alert("Your data has been saved!!!!");
            window.location.assign("/employee-transaction-grc/");
        } else {
            window.alert("An unknown error occurred");
        }
    } catch (error) {
        window.alert(error);
        console.log(error);
    }
};

// Attach the event listener to the button
var Btn_Save_inventory = document.querySelector('#Btn_Save_inventory');
Btn_Save_inventory.addEventListener("click", insert_inventory);