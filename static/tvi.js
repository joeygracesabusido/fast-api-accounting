
                
async function insertRental() {
// Get the values of the input fields
const data = {
    transDate: document.getElementById("trans_date").value,
    demr:  document.getElementById("demr_form").value,
    equipmentId: document.getElementById("equipment_id").value,
    time_in: document.getElementById("start").value,
    time_out: document.getElementById("end").value,
    totalHours: document.getElementById("total_rental_hour").value,
    rentalRate: document.getElementById("rental_rate").value,
    totalAmount: document.getElementById("rental_amount").value,
    taxRate: document.getElementById("taxRateTransaction").value,
    vat_output: document.getElementById("vatOutputRentalTrans").value,
    net_of_vat: document.getElementById("netOfVAtRentalTrans").value,
    project_site: document.getElementById("project_site").value,
    driverOperator: document.getElementById("driverOperator").value,
};
console.log(data)
// Use the fetch API to send the POST request

if (data.taxRate=='' || data.transDate == ''){
                window.alert("Please fill up Blank flieds/field"); 
            }
            else{

                try {
                        const response = await fetch(`/api-insert-tvi-rental-employeeLogin/`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(data)
                        });
                
                        // Check if the response was successful
                        if (response.status === 200) {
                        window.alert("Your data has been saved");
                        console.log(data);
                        let start = document.getElementById('start');
                        let end = document.getElementById('end');
                        let total_rental_hour = document.getElementById('total_rental_hour');
                        let rental_amount = document.getElementById('rental_amount');
                        let rental_amount2 = document.getElementById('rental_amount2');
                        let taxRateTransaction = document.getElementById('taxRateTransaction');
                        let vatOutputRentalTrans = document.getElementById('vatOutputRentalTrans');
                        let netOfVAtRentalTrans = document.getElementById('netOfVAtRentalTrans');


                        start.value = '';
                        end.value = '';
                        total_rental_hour.value = '';
                        vatOutputRentalTrans.value = '';
                        rental_amount.value = '';
                        rental_amount2.value = '';
                        taxRateTransaction.value = '';
                        netOfVAtRentalTrans.value = '';


                        // window.location.assign("/employee-transaction-tvi/");

                        
                        } else if (response.status === 401) {
                        window.alert("Unauthorized credential. Please login");
                        }
                    } catch (error) {
                        // Catch any errors and log them to the console
                        window.alert(error);
                        console.log(error);
                    }
                                    
                    }

};





function delete_rental(id){
    if (confirm("Are you sure you want to delete this record?")){
        fetch("/api-deletetiv-rental-employeeLogin/"+ id, {
            method:'DELETE',
                })
                .then(response => {
                    if (response.ok) {
                    windows.alert('Your data has been deleted');
                   
                    } else {
                    throw new Error('Failed to delete data');
                    }
                })
                .catch(error => {
                    alert(error.message);
                });
        
       
    }

    
  
}
            
// =======================================This function is for Inserting TVI Routes=============================
// Define the addtviroutes function
async function InsertRoutes() {
    // Get the values of the input fields
    const data = {
        routes: document.getElementById("routes_routes").value,
        distance: document.getElementById("distance_routes").value,
    };
    console.log(data);

    // Use the fetch API to send the POST request
    const search_url_SEARCH = `/api-get-tvi-check-routes-employeeLogin/?routes=${data.routes}`;
    const responseSEARCH = await fetch(search_url_SEARCH);
    const dataSEARCH = await responseSEARCH.json();
    console.log(dataSEARCH);

    if (dataSEARCH.length > 0) {
        window.alert("Your routes already exist");
    } else if (data.routes === '' || data.distance === '') {
        window.alert("Please fill up Blank fields/field");
    } else {
        try {
            const response = await fetch(`/api-insert-tvi-routes-employeeLogin/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            // Check if the response was successful
            if (response.status === 200) {
                window.alert("Your data has been saved");
                console.log(data);
                window.location.assign("/employee-transaction-tvi/");
            } else if (response.status === 401) {
                window.alert("Unauthorized credential. Please login");
            }
        } catch (error) {
            // Catch any errors and log them to the console
            window.alert(error);
            console.log(error);
        }
    }
}

// Attach the event listener to the button
var btnInsertRoutes = document.querySelector('#insertRoutes');
btnInsertRoutes.addEventListener("click", InsertRoutes);

// ======================================== This function is for Autho complete of equipment====================
$( function() { 
    $("#equipmentID_tons").autocomplete({
    source: "/api-search-autocomplete-tvi-equipment2/"
    });

} );


$( function() { 
    $("#routes_tons").autocomplete({
    source: "/api-search-autocomplete-tvi-routes/"
    });

} );

// ========================================This is for Displaying the Total Distance=============================
$(document).ready(function() {
    $("#routes_tons").on("keyup", async function(event) {
        // check if Enter key was pressed
        if (event.keyCode === 13) { // this is to click enter and display distance
        // trigger button click event
            var routes = document.getElementById("routes_tons").value

            const search_url = `/api-get-tvi-check-routes-employeeLogin/?routes=${routes}`;


            const responce =  await fetch(search_url)
            const data =  await responce.json();
            console.log(data)
            
            if (data.length === 0){
                window.alert(`No ID store for ${routes}`)
            }else{
                let distance = data[0].distance
                distance = parseFloat(distance).toFixed(2)
                document.getElementById("distance_tons").value = distance
                
                

            }
       
        }
    });
});       




// =======================================This function is for Inserting Tonnage ================================

// Define the InsertTons function
async function InsertTons() {
    // Get the values of the input fields
    const data = {
        transDate: document.getElementById("transDate_tons").value,
        equipmentId: document.getElementById("equipmentID_tons").value,
        tripTicket:document.getElementById("tripTicket_tons").value,
        routes: document.getElementById("routes_tons").value,
        trips: document.getElementById("trips").value,
        volume_tons: document.getElementById("volTons").value,
        distance: document.getElementById("distance_tons").value,
        hauling_rate: document.getElementById("rate_tons").value,
        project_site: document.getElementById("project_tons").value,
        driverOperator: document.getElementById("driverOperatorTons").value,
        
         
    };
    console.log(data.volume_tons);

    // Use the fetch API to send the POST request
    const search_url_SEARCH = `/api-get-tvi-check-tons-employeeLogin/?tripTicket=${data.tripTicket}`;
    const responseSEARCH = await fetch(search_url_SEARCH);
    const dataSEARCH = await responseSEARCH.json();
    console.log(dataSEARCH);

    if (dataSEARCH.length > 0) {
        window.alert("Your routes already exist");
    } else if (data.transDate == '' || data.equipmentId == '' || data.tripTicket == '' || data.distance =='') {
        window.alert("Please fill up Blank fields/field");
    } else {
        try {
            const response = await fetch(`/api-insert-tvi-tons-employeeLogin/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            // Check if the response was successful
            if (response.status === 200) {
                window.alert("Your data has been saved");
                console.log(data);
                // window.location.assign("/employee-transaction-tvi/");
            } else if (response.status === 401) {
                window.alert("Unauthorized credential. Please login");
            }
        } catch (error) {
            // Catch any errors and log them to the console
            window.alert(error);
            console.log(error);
        }
    }
}

// Attach the event listener to the button
var btnInsertTons = document.querySelector('#BtnSave_Tons');
btnInsertTons.addEventListener("click", InsertTons);


// this is for computation of 
$(document).ready(function() {
    $('#distance_tons, #volTons, #rate_tons').on('input', function() {
        calculateTonageAmount();
    });
    });

    function calculateTonageAmount() {

    var distance_tons = parseFloat($('#distance_tons').val());
    var rate_tons = parseFloat($('#rate_tons').val());
    var volume_routes = parseFloat($('#volTons').val());
    
    
    var product = volume_routes * distance_tons * rate_tons;

    // product = parseFloat(product).toFixed(2)
    var product2 = product.toLocaleString("en-US");

    $('#totalAmount_tons').val(product2);
   
    }

// document.addEventListener("DOMContentLoaded", function() {
//     var volume_tons = document.getElementById("volume_tons");
//     var distance_tons = document.getElementById("distance_tons");
//     var rate_tons = document.getElementById("rate_tons");

//     volume_tons.addEventListener("input", calculateTonageAmount);
//     distance_tons.addEventListener("input", calculateTonageAmount);
//     rate_tons.addEventListener("input", calculateTonageAmount);
// });

// function calculateTonageAmount() {
//     var volume_routes = parseFloat(document.getElementById("volume_tons").value);
//     var distance_tons = parseFloat(document.getElementById("distance_tons").value);
//     var rate_tons = parseFloat(document.getElementById("rate_tons").value);

//     var product = volume_routes * distance_tons * rate_tons;
//     var product2 = product.toLocaleString("en-US");

//     document.getElementById("totalAmount_tons").value = product2;
// }

// const rental_url =search_url ;

// =========================This function is for Displaying Data of Tons Transaction ============================
async function displayTonsData(){
    var datefrom = document.getElementById("datefrom_tons").value
    var dateto = document.getElementById("dateto_tons").value
    var equipmentID = document.getElementById("equipmentIDSearch_tons").value
    var project_site = document.getElementById("prjectSiteSearch_tons").value

    const search_url = `/api-get-tvi-tons-employeeLogin/?datefrom=${datefrom}&dateto=${dateto}&equipmentId=${equipmentID}&project_site=${project_site}`;


    const responce = await fetch(search_url)
    const data = await responce.json();
    console.log(data)

    if (data.length === 0) {
            window.alert('No Data available');
        };
    
    
    if (responce.status === 200){
        let tableData="";
        data.map((values)=>{
            tableData+= ` <tr>
                        <td>${values.id}</td>
                        <td>${values.transDate}</td>
                        <td>${values.equipmentId}</td>
                        <td>${values.tripTicket}</td>
                        <td>${values.routes}</td>
                        <td>${values.trips}</td>
                        <td>${values.volume_tons}</td>
                        <td>${values.distance}</td>
                        <td>${values.hauling_rate}</td>
                        <td>${values.billingAmount2}</td>
                        <td hidden>${values.billingAmount}</td>
                        <td>
                        <a href="/api-get-update-tvi-tonsTransaction-sqlModel/${values.id}"
                            <button type="button" class="btn btn-primary">
                        <i class="fas fa-plus-square"></i>Edit</button></a> 
                       
                        </td>
                    
                    </tr>`;
        });
        document.getElementById("table_body_tons").innerHTML=tableData;
        // var test = 1000
        // document.getElementById("fter_totalBillinglTons").value = test;
        summaryTonnageTotal()
    }else if (responce.status === 401){
        window.alert("Unauthorized Credentials Please Log in")
    }

};

//<a href="/api-get-update-tvi-rentalTransaction-sqlModel/${values.id}"

// Attach the event listener to the button
var BtnSearch_Tons = document.querySelector('#BtnSearch_Tons');
BtnSearch_Tons.addEventListener("click", displayTonsData);

// This is for total of Trips and Amount using ES
const summaryTonnageTotal = () => {
    const table = document.querySelector("#table_body_tons");
    let sumTons = 0;
    let sumTotalAmount = 0;
  
    table.querySelectorAll("tr").forEach(row => {
      sumTons += parseFloat(row.querySelectorAll("td")[5].textContent);
      sumTotalAmount += parseFloat(row.querySelectorAll("td")[10].textContent);
    });
  
    const sumTotalHoursComma = sumTons.toLocaleString("en-US");
    const sumTotalAmountComma = sumTotalAmount.toLocaleString("en-US");
  
    document.querySelector("#fter_totalTrip").value = sumTotalHoursComma;
    document.querySelector("#fter_totalBillinglTons").value = sumTotalAmountComma;
  };



//===================================This function is for Displaying Data Incentive===========================
 const  incentivesData = async () =>{
    var datefrom = document.getElementById("datefrom_incentive").value;
    var datetoTo = document.getElementById("dateto_inct").value;
    var equipmentId = document.getElementById("equipmentIDSearch_inct").value;
    
    const search_url = `/api-get-tvi-tons-incentives/?datefrom=${datefrom}&dateto=${datetoTo}&equipmentId=${equipmentId}`;
        const responce =  await fetch(search_url)
        const data =  await responce.json();
        console.log(data)

        function filterData(searchValue) {
            return data.filter(item => {
                const equipmentId = item.equipmentId.toLowerCase();
                const routes = item.routes.toLowerCase();
                const driverOperator = item.driverOperator.toLowerCase();
                return equipmentId.includes(searchValue) || routes.includes(searchValue) || driverOperator.includes(searchValue);
            });
        }

        function displayData(filteredData) {
            const tbody = document.querySelector("#table_body_incentive");
            tbody.innerHTML = "";
            filteredData.forEach(item => {
                const tr = document.createElement("tr");
                const equipmentId = document.createElement("td");
                equipmentId.textContent = item.equipmentId;
                const routes = document.createElement("td");
                routes.textContent = item.routes;
                const trips = document.createElement("td");
                trips.textContent = item.trips;
                const distance = document.createElement("td");
                distance.textContent = item.distance;
                const driverOperator = document.createElement("td");
                driverOperator.textContent = item.driverOperator;
                const incentives = document.createElement("td");
                incentives.textContent = item.incentives;
                


                tr.appendChild(equipmentId);
                tr.appendChild(routes);
                tr.appendChild(trips);
                tr.appendChild(distance);
                tr.appendChild(driverOperator);
                tr.appendChild(incentives);
                tbody.appendChild(tr);
            });
            summaryincetiveTotal()
        }

        const searchInput = document.querySelector("#autoSearch_incentive");
        searchInput.addEventListener("input", event => {
            const searchValue = event.target.value.trim().toLowerCase();
            const filteredData = filterData(searchValue);
            displayData(filteredData);
        });

};

// Attach the event listener to the button for Incentives List
var BtnSearch_incentives = document.querySelector('#BtnSearch_incentives');
BtnSearch_incentives.addEventListener("click", incentivesData);


// This is for total of Trips and Amount for incentive  using ES6
const summaryincetiveTotal = () => {
    const table = document.querySelector("#table_body_incentive");
    let sumTons = 0;
    let sumTotalAmount = 0;
  
    table.querySelectorAll("tr").forEach(row => {
      sumTons += parseFloat(row.querySelectorAll("td")[2].textContent);
      sumTotalAmount += parseFloat(row.querySelectorAll("td")[5].textContent);
    });
  
    const sumTotalHoursComma = sumTons.toLocaleString("en-US");
    const sumTotalAmountComma = sumTotalAmount.toLocaleString("en-US");
  
    document.querySelector("#flter_totalTrip_inct").value = sumTotalHoursComma;
    document.querySelector("#flter_totalIncentives").value = sumTotalAmountComma;
  };

//this is for exporting data of TVI tonnage report
