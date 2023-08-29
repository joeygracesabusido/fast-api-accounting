//  this is for computing total Rental Hours

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



// =======================================This function is for Inserting Employee ================================
    
    // Define the InsertTons function
    const  InsertEmployee = async () => {
        // Get the values of the input fields
        const data = {
            employee_id: document.getElementById("employeeID").value,
            lastName: document.getElementById("lastName").value,
            firstName: document.getElementById("firstName").value,
            middleName: document.getElementById("middleName").value,
            gender: document.getElementById("gender").value,
            address_employee: document.getElementById("address").value,
            contactNumber: document.getElementById("contactNum").value,
            contact_person: document.getElementById("conPerson").value,
            emer_cont_person: document.getElementById("emerCon").value,
            position: document.getElementById("position").value,
            date_hired: document.getElementById("dateHire").value,
            department: document.getElementById("department").value,
            end_contract: document.getElementById("endofContract").value,
            tin: document.getElementById("tin").value,
            sssNumber: document.getElementById("sss").value,
            phicNumber: document.getElementById("phic").value,
            hdmfNumber: document.getElementById("hdmf").value,
            employment_status: document.getElementById("empStatus").value,
            salary_rate: document.getElementById("salaryRate").value,
            taxCode: document.getElementById("taxcode").value,
            off_on_details: document.getElementById("on_offDetail").value,
            Salary_Detail: document.getElementById("salaryDetails").value,
            
           
            
             
        };
       
        console.log(data)
    
        if (data.employee_id == '') {
            window.alert("Please fill up Employee ID");
        } else {
            try {
                const response = await fetch(`/api-insert-employee-employeeLogin/`,{
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
    
                // Check if the response was successful
                if (response.status === 200) {
                    window.alert("Your data has been saved");
                    console.log(data);
                    window.location.assign("/employee-transaction-grc/");
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
    var Btn_employee_save = document.querySelector('#Btn_employee_save');
    Btn_employee_save.addEventListener("click", InsertEmployee);


    const  displayPayroll =  async () => {
        var datefrom = document.getElementById("datefrom_payroll").value 
        var dateto = document.getElementById("dateto_payroll").value 
        var employeeID = document.getElementById("employeeID_payroll").value 
        
        const search_url = `/grc-payroll-list-employeeLogin/?datefrom=${datefrom}&dateto=${dateto}&employeeID=${employeeID}`;


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
                // Calculate the sum of the values
                let total = parseFloat(values.regDayCal) + parseFloat(values.regDayOtCal) + 
                parseFloat(values.sundayCal) + parseFloat(values.sundayOTCal) + 
                parseFloat(values.splCal) + parseFloat(values.splOTCal) + 
                parseFloat(values.lgl2Cal) + parseFloat(values.lgl2OTCal) + 
                parseFloat(values.nightDiffCal) + parseFloat(values.lgl1Cal) +
                parseFloat(values.adjustment);
                total = total.toFixed(2)
                tableData+= ` <tr>
                            <td>${columnNumber}</td>
                            <td>${values.first_name}</td>
                            <td>${values.last_name}</td>
                            <td>${values.regDayCal}</td>
                            <td>${values.regDayOtCal}</td>
                            <td>${values.sundayCal}</td>
                            <td>${values.sundayOTCal}</td>
                            <td>${values.splCal}</td>
                            <td>${values.splOTCal}</td>
                            <td>${values.lgl2Cal}</td>
                            <td>${values.lgl2OTCal}</td>
                            <td>${values.lgl1Cal}</td>
                            <td>${values.nightDiffCal}</td>
                            <td>${values.adjustment}</td>
                            <td>${total}</td>
                            <td>
                             
                        
                            </td>
                        
                        </tr>`;
            });
            document.getElementById("table_body_payroll").innerHTML=tableData;
            // var test = 1000
            // document.getElementById("fter_totalBillinglTons").value = test;
            sumtoTalAmount()
        }else if (responce.status === 401){
            window.alert("Unauthorized Credentials Please Log in")
        }

    };


    var BtnSearch_Payroll = document.querySelector('#BtnSearch_Payroll');
    BtnSearch_Payroll.addEventListener("click", displayPayroll);


  

   
       // This is for total of Payroll for Adan in Table
    const sumtoTalAmount = () => {
        const table = document.querySelector("#table_body_payroll");
        let sumTons = 0;
        let sumTotalAmount = 0;

        table.querySelectorAll("tr").forEach(row => {
        // sumTons += parseFloat(row.querySelectorAll("td")[2].textContent);
        sumTotalAmount += parseFloat(row.querySelectorAll("td")[14].textContent);
        });

        // const sumTotalHoursComma = sumTons.toLocaleString("en-US");
        const sumTotalAmountComma = sumTotalAmount.toLocaleString("en-US");

        // document.querySelector("#flter_totalTrip_inct").value = sumTotalHoursComma;
        document.querySelector("#totalPayrollAmount").value = sumTotalAmountComma;
    };
    


    // this function is for getting List of Employee
    async function employeeData(){
        const search_url = `/api-get-grc-employeeDetails-employeeLogin/`;
            const responce =  await fetch(search_url)
            const data =  await responce.json();
            console.log(data)

            function filterData(searchValue) {
                return data.filter(item => {
                    const lastName = item.lastName.toLowerCase();
                    const firstName = item.firstName.toLowerCase();
                    const position = item.position.toLowerCase();
                    return lastName.includes(searchValue) || firstName.includes(searchValue) || position.includes(searchValue);
                });
            }

            function displayData(filteredData) {
                const tbody = document.querySelector("#table_body_employee");
                tbody.innerHTML = "";
                filteredData.forEach(item => {
                    const tr = document.createElement("tr");
                    const employee_id = document.createElement("td");
                    employee_id.textContent = item.employee_id;
                    const lastName = document.createElement("td");
                    lastName.textContent = item.lastName;
                    const firstName = document.createElement("td");
                    firstName.textContent = item.firstName;
                    const position = document.createElement("td");
                    position.textContent = item.position;
                    const department = document.createElement("td");
                    department.textContent = item.department;
                    const off_on_details = document.createElement("td");
                    off_on_details.textContent = item.off_on_details;
                    const employment_status = document.createElement("td");
                    employment_status.textContent = item.employment_status;


                    tr.appendChild(employee_id);
                    tr.appendChild(lastName);
                    tr.appendChild(firstName);
                    tr.appendChild(position);
                    tr.appendChild(department);
                    tr.appendChild(off_on_details);
                    tr.appendChild(employment_status);
                    tbody.appendChild(tr);
                });
            }

            const searchInput = document.querySelector("#searchInput");
            searchInput.addEventListener("input", event => {
                const searchValue = event.target.value.trim().toLowerCase();
                const filteredData = filterData(searchValue);
                displayData(filteredData);
            });




    }
   
    employeeData()



    // this is for  automatic end of contract function
    
    const dateInput = document.getElementById('dateHire');
    const endofContractInput = document.getElementById('endofContract');
    
    dateInput.addEventListener('input', () => {
        const selectedDate = new Date(dateInput.value);
        const maturityDays = 150; // Number of days for maturity
    
        const maturityDate = new Date(selectedDate);
        maturityDate.setDate(selectedDate.getDate() + maturityDays);
    
        const year = maturityDate.getFullYear();
        const month = String(maturityDate.getMonth() + 1).padStart(2, '0');
        const day = String(maturityDate.getDate()).padStart(2, '0');
    
        const formattedMaturityDate = `${year}-${month}-${day}`;
        endofContractInput.value = formattedMaturityDate;
    
        console.log(maturityDate);
        // Perform additional actions with the maturityDate if needed
    });


 // Define the Insert Equipment function
//  const InsertEquipment = async () => {
//     const data = {
//         equipment_id: document.getElementById("equipment_id").value,
//         equipmentDiscription: document.getElementById("equipment_description").value,
//         rentalRate: document.getElementById("rentalRate").value,
//         comments: document.getElementById("comments").value,
//         owners: document.getElementById("Owner").value,
//     };

//     try {
//         const response = await fetch(`/api-insert-grc-equipment/`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(data),
//         });

//         const responseData = await response.json();
       
//         if ("error" in responseData) {
//             window.alert("Error: " + responseData.error);
//         } else if ("message" in responseData) {
//             window.alert(responseData.message);
//             window.location.assign("/employee-transaction-grc/");
//         }
//         if (response.status === 401) {
//             window.alert("Unauthorized credential. Please login");
//         }
//     } catch (error) {
//         window.alert("Duplicate Equipment ID");
//         console.log(error);
//     }
// };


 const InsertEquipment = async () => {
    const data = {
        equipment_id: document.getElementById("equipment_id").value,
        equipmentDiscription: document.getElementById("equipment_description").value,
        rentalRate: document.getElementById("rentalRate").value,
        comments: document.getElementById("comments").value,
        owners: document.getElementById("Owner").value,
    };

    try {
        const response = await fetch(`/api-insert-grc-equipment/`, {
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

// this is for autocomplete of Equipment

// $(document).ready(function(){
//     $("#equipment_id_insertRental").autocomplete({
//             source: "/api-search-autocomplete-grc-equipment/"
//             });

//         } );

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


function html_table_excel_payroll(type){
    var data = document.getElementById('table_body_payroll');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'payrollist.' + type);

}

// this function is for inserting Rental Transaction for GRC

const insertRental = async () => {
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
        const response = await fetch(`/api-insert-grc-rental/`, {
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
            // window.location.assign("/employee-transaction-grc/");
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
    
    const search_url = `/api-get-grc-rental-transaction-employeeLogin/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;


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
                        <td>${values.demr}</td>
                        <td>${values.equipment_id}</td>
                        <td>${values.totalHours}</td>
                        <td>${values.rentalRate}</td>
                        <td>${values.amount}</td>
                        
                        
                        <td>
                            <a href="/update-rental-grc/${values.id}"
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


// this function is for exporting excel for rental transaction
function html_table_excel_payroll(type){
    var data = document.getElementById('table_body_rental');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'rentallist.' + type);

}



// =================================This is for Diesel Transactions ======================================
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

// this function is for 
    const insertDiesel = async () => {
        const data = {
            transDate: document.getElementById("transDate").value,
            withdrawal_slip: document.getElementById("eur_form").value,
            equipment_id: document.getElementById("equipment_id_insertRental").value,
            literUse: document.getElementById("total_rental_hour").value,
            price: document.getElementById("rentalRateInsertRental").value,
            amount: document.getElementById("total_amount2").value,
           
           
        };
    
        try {
            const response = await fetch(`/api-insert-grc-diesel/`, {
                method: "POST",
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
                window.alert("Your data has been saved!!!!");
                // window.location.assign("/employee-transaction-grc/");
            }
           
            
        } catch (error) {
            window.alert(error);
            console.log(error);
        }
    };
    