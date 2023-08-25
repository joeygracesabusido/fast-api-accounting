$(document).ready(function() {
    $('#start, #end').change(function() {
        const startDate = new Date($('#start').val()).getTime() || 0;
        const endDate = new Date($('#end').val()).getTime() || 0;
        const elapsed = endDate - startDate;
        const elapsedInSeconds = (elapsed / 1000) / 60 / 60;
        // console.log(startDate,elapsedInSeconds)

        totalHours = elapsedInSeconds.toFixed(2)
        $('#total_rental_hour').val(totalHours);
        calculateAmount()
        calculateAmount2();
       
    });
    });

   

    $(document).ready(function() {
        $('#total_rental_hour, #rentalRateInsertRental').on('input', function() {
            calculateAmount();
        });
        });

        function calculateAmount() {
        let product
        var totalHours = $('#total_rental_hour').val();
        var rentalRate = $('#rentalRateInsertRental').val();
        
        product = totalHours  * rentalRate;
        // product = product.toFixed(2)
        // var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
        const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        $('#total_amount').val(stringNumber);
      
        }

    $(document).ready(function() {
        $('#total_rental_hour, #rentalRateInsertRental').on('input', function() {
            calculateAmount2();
        });
        });

        function calculateAmount2() {
        let product
        var totalHours = $('#total_rental_hour').val();
        var rentalRate = $('#rentalRateInsertRental').val();
        
        product = totalHours  * rentalRate;
        // product = product.toFixed(2)
        // var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
        const stringNumber2 = product.toFixed(2)
        $('#total_amount2').val(stringNumber2);
        
        }


        $(document).ready(function() {
            $("#equipment_id_insertRental").autocomplete({
                source: function(request, response) {
                    $.ajax({
                        url: "/api-search-autocomplete-grc-equipment/",
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


        const updateRental = async () => {
            const id = document.getElementById("transID").value
            const data = {
                transDate: document.getElementById("transDate").value,
                demr: document.getElementById("eur_form").value,
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
                const response = await fetch(`/api-update-rental-grc-employeeLogin/`+ id, {
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
                    // window.location.assign("/employee-transaction-grc/");
                }
               
                
            } catch (error) {
                window.alert("Duplicate Tripticket no.");
                console.log(error);
            }
        };
        
        
        
        // Attach the event listener to the button
        var Btn_update_save = document.querySelector('#Btn_update_save');
        Btn_update_save.addEventListener("click", updateRental);