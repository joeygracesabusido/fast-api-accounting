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



// this function is for autocomplete details for Updating 
$(document).ready(function() {
    $("#trans_id").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-search-autocomplete-tiv-diesel-transaction/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                }
            });
        },
        select: function(event, ui) {
            $("#trans_id").val(ui.item.value);
            $("#trans_date").val(ui.item.transDate);
            $("#equipment_id").val(ui.item.equipmentId);
            $("#withdrawal_slip").val(ui.item.withdrawalSlip);
            $("#use_liter").val(ui.item.totalliters);
            $("#price").val(ui.item.price);
            $("#amount").val(ui.item.totalAmount);

            
            return false;
        }
    });
});


// this function is for updating Diesel by Employee Login

const update_diesel = async() => {
    var data = {}
    var id = document.getElementById("trans_id").value
    data["transDate"] = document.getElementById("trans_date").value
    data["equipmentId"] = document.getElementById("equipment_id").value
    data["withdrawalSlip"] = document.getElementById("withdrawal_slip").value
    data["totalliters"] = document.getElementById("use_liter").value
    data["price"] = document.getElementById("price").value
    data["totalAmount"] = document.getElementById("amount").value
    
   
    
    console.log(data)


    if(id != '' | data["withdrawal_slip"] != '' | data["totalAmount"] 
               | data["equipmentId"] != ''    ){

        const queryParams = new URLSearchParams();
        queryParams.append("id", id);
            
        fetch(`/api-update-tiv-diesel-employeeLogin/?${queryParams.toString()}`, {
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
                window.location.assign("/employee-transaction-tvi/");
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