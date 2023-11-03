const InsertEquipment = async () => {
    const data = {
        equipment_id: document.getElementById("equipment_id").value,
        equipmentDiscription: document.getElementById("equipment_description").value,
        rentalRate: document.getElementById("rentalRate").value,
        comments: document.getElementById("comments").value,
        owners: document.getElementById("Owner").value,
    };

    try {
        const response = await fetch(`/insert-equipment-sgmc/`, {
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
var Btn_equipment_save = document.querySelector('#Btn_SaveEquipment');
Btn_equipment_save.addEventListener("click", InsertEquipment);



// this function is for autocomplete of equipment

$(document).ready(function() {
    $("#equipment_id_insertRental").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-sgmc-equipment/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                }
            });
        },
        select: function(event, ui) {
            $("#equipment_id_insertRental").val(ui.item.value);
            $("#rentalRateInsertRental").val(ui.item.rentalRate);
            
            return false;
        }
    });
});


// this function is for autocomplete of Driver

$(document).ready(function() {
    $("#driverOperator").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-grc-employee/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                }
            });
        },
        select: function(event, ui) {

            // var concatenatedName = ui.item.value + " " + ui.item.firstname;
            // $("#driverOperator").val(concatenatedName);
            $("#driverOperator").val(ui.item.value);
            
            return false;
        }
    });
});