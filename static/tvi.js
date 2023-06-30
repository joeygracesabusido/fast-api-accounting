
                
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


//This function is for printing PDF of Tonnage
const tonsData = {
   

    company: 'LD GLOBAL LEGACY INC.',
    address: '0090 OAKLAND ST. GLORIA VISTA SUBD. SAN RAFAEL, RODRIGUEZ (MONTALBAN), RIZAL',
    tin: 'TIN: 007-241-244',

    
    
    // customer: {
    //   name: 'John Doe',
    //   address: '123 Main St, City',
    //   email: 'johndoe@example.com'
    // },
    // items: [
    //   { description: 'Product A', quantity: 2, price: 10 },
    //   { description: 'Product B', quantity: 1, price: 20 },
    //   { description: 'Product C', quantity: 3, price: 15 }
    // ]
  };
  
const generateInvoicePDF = async(tonsData) => {
    var datefrom = document.getElementById("datefrom_tons").value
    var dateto = document.getElementById("dateto_tons").value
    var equipmentID = document.getElementById("equipmentIDSearch_tons").value
    var project_site = document.getElementById("prjectSiteSearch_tons").value

    const search_url = `/api-get-tvi-tons-employeeLogin/?datefrom=${datefrom}&dateto=${dateto}&equipmentId=${equipmentID}&project_site=${project_site}`;


    const responce = await fetch(search_url)
    const items = await responce.json();
    

    const sumTotalTrips = items.reduce((total, item) => total + item.trips, 0);
    let sumTotalAmount = items.reduce((total, item) => total + item.billingAmount, 0);
    sumTotalAmount = sumTotalAmount.toLocaleString("en-US");

    
    const { company, address, tin,} = tonsData;
  
    // Create a document definition using pdfmake syntax
  
    const pageSize = {
      width: 8.5 * 72,  // Convert inches to points (1 inch = 72 points)
      height: 13 * 72
    };
    const docDefinition = {
      pageOrientation: 'portrait',
      pageSize: pageSize,
      content: [
        { text: `${company}`, style: 'header' },
        { text: `${address}`, style: 'header2' },
        { text: `${tin}`, style: 'header2' },
        ' ',
        { text: `Period: ${datefrom} to ${dateto}`,style: 'subheader' },
        
        ' ',
        { text: 'Billing Items:', style: 'subheader' },
        {
          table: {
            headerRows: 1,
            body: [
              ['#','Date', 'Equipment', 'TripTicket', 'Routes','Trips','Volume','Distance','Rate','Amount'],
              ...items.map((item, index) => [
                index + 1,
                item.transDate,
                item.equipmentId,
                item.tripTicket,
                item.routes,
                item.trips,
                item.volume_tons,
                item.distance,
                item.hauling_rate,
                item.billingAmount2,
              ])
            ]
          },
          layout: 'lightHorizontalLines',
          style: 'bodyText'
        },
        ' ',
        
        {
            columns: [
                {
                    text: `Total Trips: ${sumTotalTrips}`,
                    style: 'summaryStyle'
                },
                {
                    text: `Total Amount: ${sumTotalAmount}`,
                    style: 'totalAmount'
                }
            ],
            columnGap: 5, // Spacing between the two columns
            // margin: [0, 10, 0, 5], // Margins for the entire element
        },
        {
        columns:[
            { text: 'Prepared by:', style: 'preparedBY' },
            { text: 'Checked by:', style: 'checkedBY' },
        ],
        columnGap: 5,
        },

        ' ',
        ' ',
        { text: 'KATLEEN MAE ALBA', style: 'preparedBY' },
        { text: 'Accounting Asst', style: 'preparedBY' },

        

      ],
      styles: {
        bodyText: {
            fontSize: 9
          }, 
        header: {
          fontSize: 15,
          bold: true,
          alignment: 'center',
          margin: [25, 0, 0, 10]
        },
        header2: {
            fontSize: 10,
            bold: false,
            alignment: 'center',
            margin: [25, 0, 0, 10]
          },
        subheader: {
          fontSize: 14,
          bold: true,
          margin: [0, 10, 0, 5]
        },

        preparedBY:{
        fontSize: 10,
          alignment: 'left',
        },

        checkedBY:{
            fontSize: 10,
              alignment: 'right',
              width: '50%'
            },

        pERSON:{
        fontSize: 13,
            bold: false,
            margin: [25, 0, 0, 0],
            alignment: 'left',
        },
        summaryStyle: {
            fontSize: 10,
            bold: false,
            margin: [150, 10, 20, 5],
          
          },

        totalAmount: {
            fontSize: 10,
            bold: false,
            margin: [110, 10, 20, 1],
          
          }

      },
    //   footer: function (currentPage, pageCount) {
    //     return {
    //       columns: [
    //         [
    //       {
    //           text: 'Prepared by:',
    //           alignment: 'left',
              
    //         },
  
    //         {
    //           text: 'John Doe',
    //           alignment: 'left',
    //           margin: [25, 0, 0, 0]
    //         },
    //       ],
    //         {
    //           text: 'Checked by: Jane Smith',
    //           alignment: 'right',
    //           width: '50%'
    //         }
    //       ],
    //       margin: [40, 10],
    //       fontSize: 10
    //     };
    //   }
    };
  
    
  
    // Generate the PDF
    const pdfDocGenerator = pdfMake.createPdf(docDefinition);
    pdfDocGenerator.download('tonlist.pdf');
  }

var BtnPdf_Tons = document.querySelector('#BtnPdf_Tons');
BtnPdf_Tons.addEventListener("click", function() {
  generateInvoicePDF(tonsData);
});


// ==================================This function os for Printing PDF Tonnage ==========================================



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


// =================================This is for List of Payroll Display ===================================







//=================================This is for Printing TVI Voucher=================================


// =========================This function is for Displaying Data of Tons Transaction ============================


// const printRentalPDF = async () => {

//     var datefrom = document.getElementById("datefrom").value;
//     var dateto = document.getElementById("dateto").value;
//     var equipmentID = document.getElementById("equipment_id_searchRental").value;
  
//     const search_url = `/api-get-rental-rizal-employee_login/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;
  
//     const response = await fetch(search_url);
//     const dataSet = await response.json();
    
//       const docDefinition = {
//         pageOrientation: 'landscape',
//         content: [
//           { text: 'LD GLOBAL LEGACY', style: 'header' },
//           { text: 'EQUIPMENT RENTAL REPORT', style: 'header' },
//           { text: `COVERAGE : Date From: ${datefrom}  AND  Date TO: ${dateto}`, style: 'header' },
//           { text: '\n' },
//           {
//             table: {
//               headerRows: 1,
//               widths: ['auto', 'auto', 'auto', 'auto'],
//               body: [
//                 ['Equipment ID', 'Total Hours', 'Total Amount', 'Entries'],
//                 ...generateTableRows(dataSet),
//               ],
//             },
//             layout: {
//               defaultBorder: false,
//               paddingTop: function (i, node) { return 5; },
//               paddingBottom: function (i, node) { return 5; },
//             },
//           },
//         ],
//         styles: {
//           header: {
//             fontSize: 15,
//             bold: true,
//             alignment: 'center',
//           },
//           bodyText: {
//             fontSize: 10,
//             alignment: 'right',
//           },
//           entryText: {
//             fontSize: 9,
//             bold: false,
//             alignment: 'right',
//           },
//         },
//       };
      
//       function generateTableRows(dataSet) {
//         const rows = [];
//         const groupedData = groupDataByEquipment(dataSet);
      
//         Object.entries(groupedData).forEach(([equipmentId, equipmentData]) => {
//           rows.push([
//             equipmentId,
//             equipmentData.total_rental_hour ? equipmentData.total_rental_hour.toLocaleString("en-US") : '',
//             equipmentData.rental_amount ? equipmentData.rental_amount.toLocaleString("en-US") : '',
//             generateEntriesTable(equipmentData.entries),
//           ]);
//         });
      
//         return rows;
//       }
      
//       function groupDataByEquipment(dataSet) {
//         const groupedData = {};
//         dataSet.forEach((data) => {
//           const { equipment_id, total_rental_hour, rental_amount } = data;
//           if (!groupedData[equipment_id]) {
//             groupedData[equipment_id] = {
//             total_rental_hour: 0,
//             rental_amount: 0,
//               entries: [],
//             };
//           }
//           groupedData[equipment_id].total_rental_hour += parseFloat(total_rental_hour);
//           groupedData[equipment_id].rental_amount += parseFloat(rental_amount);
//           groupedData[equipment_id].entries.push(data);
//         });
//         return groupedData;
//       }
      
//       function generateEntriesTable(entries) {
//         const body = [
//           [
//             { text: 'ID', style: 'entryText' },
//             { text: 'Trans Date', style: 'entryText' },
//             { text: 'EUR', style: 'entryText' },
//             { text: 'Total Hours', style: 'entryText' },
//             { text: 'Rental Rate', style: 'entryText' },
//             { text: 'Rental Amount', style: 'entryText' },
//           ],
//           ...entries.map((entry) =>  [
           
//             { text: entry.id.toString(), style: 'entryText' },
//             { text: entry.transaction_date, style: 'entryText' },
//             { text: entry.eur_form, style: 'entryText' },
//             { text: entry.total_rental_hour, style: 'entryText' },
//             { text: entry.rental_rate, style: 'entryText' },
//             { text: entry.rental_amount, style: 'entryText' },
//             // entry.transaction_date,
//             // entry.eur_form,
//             // entry.total_rental_hour.toLocaleString("en-US"),
//             // entry.rental_amount.toLocaleString("en-US"),
//           ]),

        

          

//         ];
      
//         return {
//           table: {
//             widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto'],
//             body,
//           },
//           layout: 'lightHorizontalLines',
//         };
//       }

      
      
//       const pdfDoc = pdfMake.createPdf(docDefinition);
//       pdfDoc.download('equipment_hauling_report.pdf');
      
// }

// const BTN_printRentalPDF = document.querySelector('#printRentalPDF');
// BTN_printRentalPDF.addEventListener("click", printRentalPDF);  

// This is for printing Tonnage PDF per Equipment
const displayTonnageData_print = async () => {
    var dateFrom = document.getElementById('datefrom_tons').value;
    var dateTo = document.getElementById('dateto_tons').value;
    var equipmentIDSearch = document.getElementById('equipmentIDSearch_tons').value;
    var project_site = document.getElementById("prjectSiteSearch_tons").value

    const search_url = `/api-get-tvi-tons-employeeLogin/?datefrom=${dateFrom}&dateto=${dateTo}&equipmentId=${equipmentIDSearch}&project_site=${project_site}`;

    // const search_url = `/api-get-tvi-tons-employeeLogin/?datefrom=${dateFrom}&dateto=${dateTo}&equipmentId=${equipmentIDSearch}&equipmentId=${equipmentIDSearch}`;

    const response = await fetch(search_url);
    const dataSet = await response.json();

    console.log(dataSet)
    const docDefinition = {
        pageOrientation: 'landscape',
        content: [
        { text: 'LD GLOBAL LEGACY', style: 'header' },
        { text: 'EQUIPMENT HAULING REPORT', style: 'header' },
        { text: `Date From:  ${dateFrom}`  , style: 'header' },
        { text: `Date   To :  ${dateTo}`  , style: 'header' },
        { text: '\n' },
        {
            table: {
            headerRows: 1,
            widths: ['auto', 'auto', 'auto', 'auto', 'auto'],
            body: [
                ['Equipment ID', 'Total Trip', 'Total Tonnage', 'Total Amount', 'Entries'],
                ...generateTableRows(dataSet),
            ],
            },
            layout: {
            defaultBorder: false,
            paddingTop: function (i, node) { return 5; },
            paddingBottom: function (i, node) { return 5; },
            },
        },
        ],
        styles: {
        header: {
            fontSize: 15,
            bold: true,
            alignment: 'center',
        },
        bodyText: {
            fontSize: 10,
            alignment: 'right',
        },
        entryText: {
            fontSize: 10,
        },
        },
    };

    

    function generateTableRows(dataSet) {
        let totalTrips = 0;
        let totalVolumeTons = 0;
        let totalBillingAmount = 0;
        const rows = [];
        const groupedData = groupDataByEquipment(dataSet);

        Object.entries(groupedData).forEach(([equipmentId, equipmentData]) => {
        rows.push([
            equipmentId,
            equipmentData.trips.toLocaleString("en-US"),
            equipmentData.volume_tons.toLocaleString("en-US"),
            equipmentData.billingAmount.toLocaleString("en-US"),
            generateEntriesTable(equipmentData.entries),
        ]);
        totalTrips += equipmentData.trips;
        totalVolumeTons += equipmentData.volume_tons;
        totalBillingAmount += equipmentData.billingAmount;
        });

              // Add a row for the grand totals
          rows.push([
            'Grand Total',
            totalTrips.toLocaleString("en-US"),
            totalVolumeTons.toLocaleString("en-US"),
            totalBillingAmount.toLocaleString("en-US"),
            '',
        ]);
        // equipmentData.totalAmount.toLocaleString("en-US"),
        return rows;
    }

    function groupDataByEquipment(dataSet) {
        const groupedData = {};
        dataSet.forEach((data) => {
        const { equipmentId, trips, volume_tons, billingAmount } = data;
        if (!groupedData[equipmentId]) {
            groupedData[equipmentId] = {
            trips: 0,
            volume_tons: 0,
            billingAmount: 0,
            entries: [],
            };
        }
        groupedData[equipmentId].trips += parseFloat(trips);
        groupedData[equipmentId].volume_tons += parseFloat(volume_tons);
        groupedData[equipmentId].billingAmount += parseFloat(billingAmount);
        groupedData[equipmentId].entries.push(data);
        });
        return groupedData;
    }

    function generateEntriesTable(entries) {
        const body = [
        [
            { text: 'ID', style: 'entryText' },
            { text: 'Trans Date', style: 'entryText' },
            { text: 'Trip Ticket', style: 'entryText' },
            { text: 'Routes', style: 'entryText' },
            { text: 'Total Trip', style: 'entryText' },
            { text: 'Tons', style: 'entryText' },
            { text: 'Rate', style: 'entryText' },
            { text: 'Amount', style: 'entryText' },
        ],
        ];

        entries.forEach((entry) => {
            console.log(entries)
        body.push([
            { text: entry.id.toString(), style: 'entryText' },
            { text: entry.transDate, style: 'entryText' },
            { text: entry.tripTicket, style: 'entryText' },
            { text: entry.routes, style: 'entryText' },
            { text: entry.trips, style: 'entryText' },
            { text: entry.volume_tons, style: 'entryText' },
            { text: entry.hauling_rate, style: 'entryText' },
            { text: entry.billingAmount.toFixed(2), style: 'entryText' },
        ]);
        });

        return {
        table: {
            widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto','auto', 'auto'],
            body,
        },
        layout: 'lightHorizontalLines',
        };
    }

    const pdfDoc = pdfMake.createPdf(docDefinition);
    pdfDoc.download('tonnagelist.pdf');
    }

const Btn_pdf_Tons = document.querySelector('#Btn_pdf_Tons');
Btn_pdf_Tons.addEventListener("click", displayTonnageData_print); 


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