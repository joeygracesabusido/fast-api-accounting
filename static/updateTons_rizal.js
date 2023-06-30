$(document).ready( function() {
                    
    $( "#equipment_id" ).autocomplete({
    source: "/api-search-autocomplete-equipment-rizal/",
    minLength: 1
    });
} );


$(document).ready(function() {
    $('#bucket_Tons, #totalTons_Tons').on('input', function() {
        calculateTotalTons();
    });
    });

    function calculateTotalTons() {

    var Backhoe = $('#Backhoe').val();
    var Bucket = $('#bucket_Tons').val();
    var bachoeValue = 0
    if (Backhoe === 'BH 01' || Backhoe === 'BH 03' ){
        bachoeValue = 2.29
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }else if(Backhoe === 'BH 02'){
        bachoeValue = 1.42
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }
    else if(Backhoe === 'TX 1202' || Backhoe === 'TX 1204'){
        bachoeValue = 1.44
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }

   
    }


$(document).ready(function() {
    $('#totalTons_Tons, #rate_Tons').on('input', function() {
        calculateProduct_amountTons();
    });
    });

    function calculateProduct_amountTons() {

    var totalTons_Tons = $('#totalTons_Tons').val();
    
    var rate_Tons = $('#rate_Tons').val();
    
    var product = totalTons_Tons * rate_Tons;
    
    var product2 = parseFloat(product).toFixed(2)

    $('#amount_Tons').val(product2);
    }



$(document).ready(function() {
    $('#rate_Tons, #totalTons_Tons').on('input', function() {
        calculateProduct_amountTons2();
    });
    });

    function calculateProduct_amountTons2() {

    var totalTons_Tons = $('#totalTons_Tons').val();
    
    var rate_Tons = $('#rate_Tons').val();
    
    var product = totalTons_Tons * rate_Tons;
    
    // var floatValue = product.toLocaleString('en-US');
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#amount_Tons2').val(stringNumber);
    }




const update_Tons = async () => {
    var data = {};
    var id = document.getElementById("transID").value;
    

    data["transDate"] = document.getElementById("transDate").value;
    data["equipment_id"] = document.getElementById("equipment_id").value;
    data["tripTicket"] = document.getElementById("tripTicket_Tons").value;
    data["totalTrip"] = document.getElementById("totalTrip_Tons").value;
    data["totalTonnage"] = document.getElementById("totalTons_Tons").value;
    data["rate"] = document.getElementById("rate_Tons").value;
    data["amount"] = document.getElementById("amount_Tons").value;
    data["driverOperator"] = document.getElementById("driverOperator").value;
    


    console.log(data);

    const inputs = document.querySelectorAll('input');
    console.log(inputs)
    let isFilled = true;
    inputs.forEach((input) => {
      if (input.value === '') {
        isFilled = false;
        return;
      }
    });

    // Converting NodeList to an array and iterating over it
    // let isFilled = true
    // Array.from(inputs).forEach((input) => {
    //     const value = input.value;
    //     // console.log(value);
    //     if (value == ''){
           
    //         isFilled = false;
    //         return;
    //     } 
        
    // });

    // const isFilled = Array.from(inputs).some((input) => input.value === '');

    

    if (isFilled) {
        try {
            // Use template literals to build the URL
            if (confirm('Are you sure you want to update this tons transaction?')){
                    const response = await fetch("/api-update-tonnage-haul-employeeLogin/"+ id, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                    });

                    // Use response.ok to check if the response was successful
                    if (response.ok) {
                    window.alert("Your Data has been Updated");
                    window.location.assign("/employee-rizal-equipment-rental/");
                    // console.log(await response.json());
                    } else if (response.status === 401) {
                    window.alert("Unauthorized credential Please Login");
                    }

            } else {
                    throw new Error('Failed to update data');
                    }
        
        } catch (error) {
                // Catch errors
                window.alert(error);
                console.log(error);
        }
        }else{
            window.alert('Please fill up blank fields')
        }
    

}
           
   

// Attach the event listener to the button for Update Tons
var Btn_update_tons = document.querySelector('#Btn_update_tons');
Btn_update_tons.addEventListener("click", update_Tons);