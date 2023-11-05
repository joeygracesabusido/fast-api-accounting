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

// this function is for inserting Rental Transaction for GRC

const insertRental = async () => {
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
        const response = await fetch(`/api-insert-sgmc-rental/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();
        console.log(responseData);
        
        if (responseData.error) {
            // Error occurred on the server side
            if (responseData.error === "Duplicate entry for DEMR") {
                window.alert("Error: Duplicate entry for DEMR");
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
var Btn_rental_save = document.querySelector('#Btn_rental_save');
Btn_rental_save.addEventListener("click", insertRental);


// this function is for displaying Rental Transaction 
const  displayRental =  async () => {
    var datefrom = document.getElementById("datefrom_rental").value || ''
    var dateto = document.getElementById("dateto_rental").value || ''
    var equipmentID = document.getElementById("equipmentID_rental").value || ''
    
    const search_url = `/api-get-sgmc-rental-transaction/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;


    const responce = await fetch(search_url)
    const data = await responce.json();
    console.log(data)

    if (data.length === 0) {
            window.alert('No Data available');
        };
    
    
    if (responce.status === 200){
        let tableData="";
        let sum = 0;
        data.map((values, index)=>{
            const columnNumber = index + 1; 
            
            tableData+= ` <tr>
                        <td>${columnNumber}</td>
                        <td>${values.id}</td>
                        <td>${values.transDate}</td>
                        <td>${values.eur}</td>
                        <td>${values.equipment_id}</td>
                        <td>${values.totalHours}</td>
                        <td>${values.rentalRate}</td>
                        <td>${values.amount}</td>
                        
                        
                        <td>
                            <a href="/update-rental-sgmc/${values.id}"
                            <button type="button" class="btn btn-primary">
                            <i class="fas fa-database"></i> Edit</button></a> 
                    
                        </td>
                    
                    </tr>`;
        });
        document.getElementById("table_body_rental").innerHTML=tableData;
        // var test = 1000
        // document.getElementById("fter_totalBillinglTons").value = test;
        sumtoTalAmountRental()
    }else if (responce.status === 401){
        window.alert("Unauthorized Credentials Please Log in")
    }

};


var BtnSearch_Rental = document.querySelector('#BtnSearch_Rental');
BtnSearch_Rental.addEventListener("click", displayRental);


   // This is for total of Rental 
   const sumtoTalAmountRental = () => {
    const table = document.querySelector("#table_body_rental");
    let sumTotalHours = 0;
    let sumTotalAmount = 0;

    table.querySelectorAll("tr").forEach(row => {
        sumTotalHours += parseFloat(row.querySelectorAll("td")[5].textContent);
        sumTotalAmount += parseFloat(row.querySelectorAll("td")[7].textContent);
    });

    // const sumTotalHoursComma = sumTons.toLocaleString("en-US");
    const sumTotalHoursComma = sumTotalHours.toLocaleString("en-US");
    const sumTotalAmountComma = sumTotalAmount.toLocaleString("en-US");

    // document.querySelector("#flter_totalTrip_inct").value = sumTotalHoursComma;
    document.querySelector("#totalamount_rental").value = sumTotalAmountComma;
    document.querySelector("#totalHours_rental").value = sumTotalHoursComma;
};


