$(document).ready( function() {
                    
    $( "#equipment_id" ).autocomplete({
    source: "/api-search-autocomplete-equipment-rizal/",
    minLength: 1
    });
} );



 $(document).ready(function() {
    $('#price, #use_liter').on('input', function() {
        calculatetotalAmount();
    });
    });

    function calculatetotalAmount() {
    let product
    var price = $('#price').val() || 0 ;
    var liter = $('#use_liter').val() || 0;
    
    product = price  * liter ;
    product = product.toFixed(2)
    $('#amount').val(product);
    
    }

// this function is for updating Diesel by Employee Login

const update_diesel = async() => {
        var data = {}
        var id = document.getElementById("trans_id").value
        data["transaction_date"] = document.getElementById("trans_date").value
        data["equipment_id"] = document.getElementById("equipment_id").value
        data["withdrawal_slip"] = document.getElementById("withdrawal_slip").value
        data["use_liter"] = document.getElementById("use_liter").value
        data["price"] = document.getElementById("price").value
        data["amount"] = document.getElementById("amount").value

       
        
        console.log(data)


        if(id != '' | data["withdrawal_slip"] != '' | data["amount"] 
                   | data["equipment_id"] != ''    ){
                
            fetch(`/api-update-diesel-employeeLogin2/`+ id, {
            method:'PUT', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
                })
            // window.location.assign("/peso-bill/");
            .then(function (response) {
                // Save the response status in a variable to use later.
                fetch_status = response.status;
                // Handle success
                // eg. Convert the response to JSON and return
                return response.json();
            }) 
            .then(function (json) {
                // Check if the response were success
                if (fetch_status == 200) {
                    // Use the converted JSON
                    window.alert("Your Data has been Updated");
                    window.location.assign("/employee-rizal-equipment-rental/");
                    console.log(json);
                }
            })
            .catch(function (error){
                // Catch errors
                window.alert(error);
                console.log(error);
            });
            
            }
            else{
                window.alert("Please fill up fields");
            }

       
    }

const Btn_updateDiesel = document.querySelector('#Btn_update_diesel');
Btn_updateDiesel.addEventListener("click", update_diesel); 
    
