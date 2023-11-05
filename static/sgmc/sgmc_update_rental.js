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

//this function is for calculating total hours for EUR
$(document).ready(function() {
    $('#start, #end').on('input', function() {
        calculate_total_hours();
    });
    });

    function calculate_total_hours() {
    let product
    var total_start = $('#start').val();
    var total_end = $('#end').val();
    
    product = total_end  - total_start;
    // product = product.toFixed(2)
    // var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_rental_hour').val(product.toFixed(2));
    calculate_total_amount();
  
    }


//this function is for calculating total amount
$(document).ready(function() {
    $('#total_rental_hour, #rentalRateInsertRental').on('input', function() {
        calculate_total_amount();
    });
    });

    function calculate_total_amount() {
    let product
    var total_rental_hr = $('#total_rental_hour').val();
    var rerntal_rate = $('#rentalRateInsertRental').val();
    
    product = total_rental_hr * rerntal_rate;
    // product = product.toFixed(2)
    // var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_amount').val(stringNumber);
    $('#total_amount2').val(product.toFixed(2));
  
    }

// this function is for updating Rental

const updateRental = async () => {
    const id = document.getElementById("transID").value
    const data = {
        transDate: document.getElementById("transDate").value,
        eur: document.getElementById("eur").value,
        equipment_id: document.getElementById("equipment_id_insertRental").value,
        timeIn: document.getElementById("start").value,
        timeOut: document.getElementById("end").value,
        totalHours: document.getElementById("total_rental_hour").value,
        rentalRate: document.getElementById("rentalRateInsertRental").value,
        amount: document.getElementById("total_amount2").value,
        shift: document.getElementById("shift").value,
        driver_operator: document.getElementById("driverOperator").value,
       
    };

    try {
        const response = await fetch(`/api-update-rental-sgmc/`+ id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);
        
        if (responseData.error) {
            // Error occurred on the server side
            if (responseData.error === "Duplicate entry for DEMR") {
                window.alert("Error: Error!!!");
            } else if (response.status === 401) {
                window.alert("Unauthorized credential. Please login");
            }
            else {
                window.alert("Error: " + responseData.error);
            }
        } else {
            
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            window.location.assign("/employee-transaction-sgmc/");
        }
       
        
    } catch (error) {
        window.alert("Duplicate Tripticket no.");
        console.log(error);
    }
};



// Attach the event listener to the button
var Btn_update_save = document.querySelector('#Btn_update_save');
Btn_update_save.addEventListener("click", updateRental);
