// this function is for calculation of Diesel Amount
$(document).ready(function() {
    $('#literUse_diesel, #price_diesel').on('input', function() {
        calculateDiesel();
    });
    });

    function calculateDiesel() {
    let product
    var liters = $('#literUse_diesel').val() || 0;
    var price = $('#price_diesel').val() || 0;
    
    product = liters  * price;
    // product = product.toFixed(2)
    var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "Php" });
    const stringNumber2 = product.toFixed(2)
    $('#amount_diesel').val(formattedAmount);
    $('#amount_diesel2').val(stringNumber2);
    
    }


//  this function is for autocompleete of Equipment
    $(document).ready(function() {
        $("#equipment_id_diesel").autocomplete({
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
                $("#equipment_id_diesel").val(ui.item.value);
               
                
                return false;
            }
        });
    });


// this function is for updating Diesel Transactions


    const updateDiesel = async () => {
        const id = document.getElementById("transID").value
        const data = {
            transDate: document.getElementById("transDate_diesel").value,
            withdrawal_slip: document.getElementById("withdrawal_slip_diesel").value,
            equipment_id: document.getElementById("equipment_id_diesel").value,
            literUse: document.getElementById("literUse_diesel").value,
            price: document.getElementById("price_diesel").value,
            amount: document.getElementById("amount_diesel2").value,
           
           
        };
        console.log(data)
    
        try {
            const response = await fetch(`/api-update-diesel-grc-employeeLogin/`+ id, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
    
            const responseData = await response.json();
            console.log(responseData);
            
            if (responseData.error) {
                // Error occurred on the server side
                if (responseData.error === "Duplicate entry for Withdrawal Slip") {
                    window.alert("Error: Duplicate entry for Withdrawal Slip");
                } 
                else {
                    window.alert("Error: " + responseData.error);
                }
            }else if (response.status === 401) {
                window.alert("Unauthorized credential. Please login");
            }
             else {
                // Data saved successfully
                window.alert("Your data has been updated!!!!");
                window.location.assign("/employee-transaction-grc/");
            }
           
            
        } catch (error) {
            window.alert(error);
            console.log(error);
        }
    };

    var Btn_update_diesel = document.querySelector('#Btn_update_diesel');
    Btn_update_diesel.addEventListener("click", updateDiesel);



