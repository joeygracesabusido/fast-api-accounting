$(document).ready(function() {
    $("#equipment_id_cost").autocomplete({
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
            $("#equipment_id_cost").val(ui.item.value);
            $("#equip_id_cost").val(ui.item.id);
            
            return false;
        }
    });
});


// this function is for updating Cost Transactions


const update_cost2 = async () => {
    const id = document.getElementById("transID").value
    const data = {
        transDate: document.getElementById("trans_date_cost").value,
        equipment_id: document.getElementById("equip_id_cost").value,
        cost_details: document.getElementById("cost_details").value,
        particular: document.getElementById("particular_cost").value,
        amount: document.getElementById("amount_cost").value,
       
       
       
    };
    console.log(data)

    try {
        const response = await fetch(`/api-update-cost-grc/`+ id, {
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

var Btn_update_cost = document.querySelector('#Btn_update_cost_grc');
Btn_update_cost.addEventListener("click", update_cost2);
