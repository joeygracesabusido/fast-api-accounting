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

// this function is for printing PDF for rental Report

const printRentalPDF = async () => {

    var datefrom = document.getElementById("datefrom_rental").value;
    var dateto = document.getElementById("dateto_rental").value;
    var equipmentID = document.getElementById("equipmentID_rental").value;
  
    const search_url = `/api-get-sgmc-rental-transaction/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;
  
    const response = await fetch(search_url);
    const dataSet = await response.json();
    
      const docDefinition = {
        pageOrientation: 'landscape',
        content: [
          { text: 'LD GLOBAL LEGACY, INC.', style: 'header' },
          { text: 'EQUIPMENT RENTAL REPORT', style: 'header' },
          { text: `COVERAGE : Date From: ${datefrom}  AND  Date TO: ${dateto}`, style: 'header' },
          { text: '\n' },
          {
            table: {
              headerRows: 1,
              widths: ['auto', 'auto', 'auto', 'auto'],
              body: [
                ['Equipment ID', 'Total Hours', 'Total Amount', 'Entries'],
                ...generateTableRows(dataSet),
              ],
            },
            layout: {
              defaultBorder: false,
              paddingTop: function (i, node) { return 5; },
              paddingBottom: function (i, node) { return 5; },
            },
          },

          { text: '\n' },
// this start of signatories
          {
            columns: [
              // "Prepared by" section
              {
                width: 'auto',
                stack: [
                  { text: 'Prepared by:', style: 'right_side_task' },
                  { text: 'MARIA LOIDA YANA', style: 'right_side_name_desig' },
                  { text: 'Billing/Accounting', style: 'right_side_name_desig' }, // You can add additional empty lines if needed
                ],
              },

              

      
              // "Reconciled by" section
              {
                width: 'auto',
                stack: [
                  { text: 'Reconciled by:', style: 'reconcilled_by' },
                  { text: 'JAYFFE AGUILAR', style: 'reconcilled_by_person' },
                  { text: 'MOTORPOOL BILLING OFFICER', style: 'reconcilled_by_person' },
                ],
              },


                // "Noted by" section
             {
                width: 'auto',
                stack: [
                  { text: 'Noted  by:',style: 'right_side_task' },
                  { text: 'ARIEL GACES', style: 'right_side_name_desig' },
                  { text: 'LD Global - Officer in Charge', style: 'right_side_name_desig' },
                ],
              },

              
            ],


        
          },

          { text: '\n' },
          {
          columns: [
          

             // "Noted by" section
             

            // "Reconciled by" section
            {
                width: 'auto',
                stack: [
                    { text: 'Verified  by:',style: 'right_side_task' },
                    { text: 'ENGR. REDZEL PARANAS', style: 'right_side_name_desig' },
                    { text: 'MOTORPOOL MANAGER', style: 'right_side_name_desig' },
                 
                ],
              },


              {
                width: 'auto',
                stack: [
                  
                  { text: 'Recommending Approval:', style: 'recomend_by' },
                  { text: 'ENGR. FITZGERALD CANAREZ', style: 'recomend_by_person' },
                  { text: 'PROJECT MINE MANAGER', style: 'recomend_by_person' },
                ],
              },


                 // "Noted by" section
             {
                width: 'auto',
                stack: [
                  { text: 'Approval:',style: 'approval' },
                  { text: 'ENGR. TEODORO C. LICTAG', style: 'approval_person' },
                  { text: 'SGMC-MINE RESIDENT MANAGER', style: 'approval_person' },
                ],
              },

          
          ],

        },

        { text: '\n' },
          {
          columns: [
          

             // "Verified  by" section
             {
              width: 'auto',
              stack: [
                { text: 'Reviewed by:',style: 'reviewed' },
                { text: 'RAYMOND C. SINOC', style: 'reviewed_person' },
                { text: 'SGMC - BILLING OFFICER', style: 'reviewed_person' },
              ],
            },

           

          
          ],

        },


        
         

        
// this is the part of 
        ],

        margin: [0, 0, 0, 0],
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
            fontSize: 11,
            bold: false,
            alignment: 'right',
          },

        // this is for right side task 
        right_side_task: { 
            fontSize: 11,
            bold: false,
            margin: [20, 0, 0, 0],
          },

        right_side_name_desig: {
            fontSize: 11,
            bold: false,
            margin: [50, 0, 0, 0],
          },


        //   this is for left side task
          left_side_task: { 
            fontSize: 11,
            bold: false,
            margin: [220, 0, 0, 0],
          },

          left_side_task_2nd: {
            fontSize: 11,
            bold: false,
            margin: [180, 0, 0, 0],
          },

          left_side_task_3rd: {
            fontSize: 11,
            bold: false,
            margin: [365, 0, 0, 0],
          },

          left_side_name_desig: {
            fontSize: 11,
            bold: false,
            margin: [270, 0, 0, 0],
          },

          left_side_name_desig_2nd: {
            fontSize: 11,
            bold: false,
            margin: [230, 0, 0, 0],
          },

          left_side_name_desig_3rd: {
            fontSize: 11,
            bold: false,
            margin: [415, 0, 0, 0],
          },


          reconcilled_by: { 
            fontSize: 11,
            bold: false,
            margin: [110, 0, 0, 0],
          },


          reconcilled_by_person: { 
            fontSize: 11,
            bold: false,
            margin: [160, 0, 0, 0],
          },


          recomend_by: { 
            fontSize: 11,
            bold: false,
            margin: [70, 0, 0, 0],
          },


          recomend_by_person: { 
            fontSize: 11,
            bold: false,
            margin: [110, 0, 0, 0],
          },


          approval: { 
            fontSize: 11,
            bold: false,
            margin: [50, 0, 0, 0],
          },

        approval_person: {
            fontSize: 11,
            bold: false,
            margin: [80, 0, 0, 0],
          },


          reviewed: { 
            fontSize: 11,
            bold: false,
            margin: [485, 0, 0, 0],
          },

          reviewed_person: {
            fontSize: 11,
            bold: false,
            margin: [515, 0, 0, 0],
          },

          
        },
      };
      
      function generateTableRows(dataSet) {
        const rows = [];
        const groupedData = groupDataByEquipment(dataSet);
      
        Object.entries(groupedData).forEach(([equipmentId, equipmentData]) => {
          rows.push([
            equipmentId,
            equipmentData.totalHours ? equipmentData.totalHours.toLocaleString("en-US") : '',
            equipmentData.amount ? equipmentData.amount.toLocaleString("en-US") : '',
            generateEntriesTable(equipmentData.entries),
          ]);
        });
      
        return rows;
      }
      
      function groupDataByEquipment(dataSet) {
        const groupedData = {};
        dataSet.forEach((data) => {
          const { equipment_id, totalHours, amount } = data;
          if (!groupedData[equipment_id]) {
            groupedData[equipment_id] = {
                totalHours: 0,
            amount: 0,
              entries: [],
            };
          }
          groupedData[equipment_id].totalHours += parseFloat(totalHours);
          groupedData[equipment_id].amount += parseFloat(amount);
          groupedData[equipment_id].entries.push(data);
        });
        return groupedData;
      }
      
      function generateEntriesTable(entries) {
        const body = [
          [
            { text: 'ID', style: 'entryText' },
            { text: 'Trans Date', style: 'entryText' },
            { text: 'EUR', style: 'entryText' },
            { text: 'Total Hours', style: 'entryText' },
            { text: 'Rental Rate', style: 'entryText' },
            { text: 'Rental Amount', style: 'entryText' },
          ],
          ...entries.map((entry) =>  [
           
            { text: entry.id.toString(), style: 'entryText' },
            { text: entry.transDate, style: 'entryText' },
            { text: entry.eur, style: 'entryText' },
            { text: entry.totalHours, style: 'entryText' },
            { text: entry.rentalRate, style: 'entryText' },
            { text: entry.amount, style: 'entryText' },
          
          ]),

        

          

        ];
      
        return {
          table: {
            widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto'],
            body,
          },
          layout: 'lightHorizontalLines',
        };
      }

      

      
      
      const pdfDoc = pdfMake.createPdf(docDefinition);
      pdfDoc.download('rental_report.pdf');
      
}

const BTN_printRentalPDF = document.querySelector('#printRentalPDF');
BTN_printRentalPDF.addEventListener("click", printRentalPDF);



const print_rental_report_PDF = async () => {

  var datefrom = document.getElementById("datefrom_rental").value;
  var dateto = document.getElementById("dateto_rental").value;
  
  console.log(dateto)
  const search_url = `/api-get-sgmc-rental-report-list/?datefrom=${datefrom}&dateto=${dateto}`;

  const response = await fetch(search_url);
  const data = await response.json();
  console.log(data)

  // Create document definition
  const documentDefinition = {
    content: [
      { text: 'LD GLOBAL LEGACY, INC.', style: 'header' },
      { text: 'EQUIPMENT RENTAL REPORT', style: 'header' },
      { text: `COVERAGE : Date From: ${datefrom}  AND  Date TO: ${dateto}`, style: 'header' },
      { text: '\n' },
        {
            table: {
                headerRows: 1,
                body: [
                    ['Equipment ID', 'Total Hours'],
                    ...data.rentalData.map(entry => [entry.equipment_id, entry.totalHours])
                ]
            }
        },
        { text: ` Grand Total Hours: ${data.totalHoursRunningTotal}`, style: 'total' }
    ],
    styles: {
        header: {
            fontSize: 15,
            bold: true,
            margin: [0, 0, 0, 0]
        },
        total: {
            fontSize: 16,
            bold: false,
            margin: [0, 10, 0, 0]
        }
    }
};
const pdfDoc = pdfMake.createPdf(documentDefinition);
pdfDoc.download('rental_report_summary.pdf');
}

const BTN_print_report_sum_PDF = document.querySelector('#print_rental_report_sum');
BTN_print_report_sum_PDF.addEventListener("click", print_rental_report_PDF);




function html_table_excel_rental(type){
    var data = document.getElementById('table_body_rental');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'rentallist.' + type);

}



// ======================================Diesel Transaction==============================

// this is for autocomplete of equipment for diesel


$(document).ready(function() {
    $("#equipment_id_diesel").autocomplete({
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
            $("#equipment_id_diesel").val(ui.item.value);
            $("#equip_id").val(ui.item.id);
            
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

// this function is for Inserting Diesel
    const insertDiesel = async () => {
        const data = {
            transDate: document.getElementById("transDate_diesel").value,
            withdrawal_slip: document.getElementById("withdrawal_slip_diesel").value,
            equipment_id: document.getElementById("equip_id").value,
            literUse: document.getElementById("literUse_diesel").value,
            price: document.getElementById("price_diesel").value,
            amount: document.getElementById("amount_diesel2").value,
           
           
        };
        console.log(data)
    
        try {
            const response = await fetch(`/api-insert-diesel-sgmc/`, {
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
                window.location.assign("/employee-transaction-sgmc/");
            }
           
            
        } catch (error) {
            window.alert(error);
            console.log(error);
        }
    };

    var BtnSave_diesel = document.querySelector('#Btn_diesel_save');
    BtnSave_diesel.addEventListener("click", insertDiesel);


    // this function is for displaying Diesel Transaction 
    const  displayDiesel =  async () => {
        var datefrom = document.getElementById("datefrom_diesel").value || ''
        var dateto = document.getElementById("dateto_diesel").value || ''
        var equipmentID = document.getElementById("equipmentID_diesel").value || ''
        
        const search_url = `/api-get-sgmc-diesel-transaction/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;
    
    
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
                            <td>${values.withdrawal_slip}</td>
                            <td>${values.equipment_id}</td>
                            <td>${values.literUse}</td>
                            <td>${values.price}</td>
                            <td>${values.amount}</td>
                            
                            
                            <td>
                                <a href="/update-diesel-sgmc/${values.id}"
                                <button type="button" class="btn btn-primary">
                                <i class="fas fa-database"></i> Edit</button></a> 
                        
                            </td>
                        
                        </tr>`;
            });
            document.getElementById("table_body_diesel").innerHTML=tableData;
            // var test = 1000
            // document.getElementById("fter_totalBillinglTons").value = test;
            sumtoTalAmountDiesel()
        }else if (responce.status === 401){
            window.alert("Unauthorized Credentials Please Log in")
        }
    
    };
    
    
    var BtnSearch_Diesel = document.querySelector('#BtnSearch_diesel');
    BtnSearch_Diesel.addEventListener("click", displayDiesel);
    
    
       // This is for total of Rental 
       const sumtoTalAmountDiesel = () => {
        const table = document.querySelector("#table_body_diesel");
        let sumTotalLiterrs = 0;
        let sumTotalAmount = 0;
    
        table.querySelectorAll("tr").forEach(row => {
            sumTotalLiterrs += parseFloat(row.querySelectorAll("td")[5].textContent);
            sumTotalAmount += parseFloat(row.querySelectorAll("td")[7].textContent);
        });
    
        // const sumTotalHoursComma = sumTons.toLocaleString("en-US");
        const sumTotalLitersComa= sumTotalLiterrs.toLocaleString("en-US");
        const sumTotalAmountComma = sumTotalAmount.toLocaleString("en-US");
    
        // document.querySelector("#flter_totalTrip_inct").value = sumTotalHoursComma;
        document.querySelector("#totalLtrs_diesel").value = sumTotalLitersComa;
        document.querySelector("#totalamount_diesel").value = sumTotalAmountComma;
    };
    

//  this function is for exporting excel for diesel transaction


function html_table_excel_diesel(type){
    var data = document.getElementById('table_body_diesel');
    var file = XLSX.utils.table_to_book(data,{sheet: "sheet1"});
    XLSX.write(file,{ booktype: type, bookSST: true, type: 'base64'});
    XLSX.writeFile(file, 'diesellist.' + type);

}


$(document).ready(function() {
  $("#equipment_id_cost").autocomplete({
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
          $("#equipment_id_cost").val(ui.item.value);
          $("#equip_id_cost").val(ui.item.id);
          
          return false;
      }
  });
});

// this function is for Inserting cost for sgmc
const insert_cost = async () => {
  const data = {
      transDate: document.getElementById("trans_date_cost").value,
      equipment_id: document.getElementById("equip_id_cost").value,
      cost_details: document.getElementById("cost_details").value,
      amount: document.getElementById("amount_cost").value,
      particular: document.getElementById("particular_cost").value,
      
     
     
  };
  console.log(data)

  try {
      const response = await fetch(`/api-insert-cost-sgmc/`, {
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
          window.location.assign("/employee-transaction-sgmc/");
      }
     
      
  } catch (error) {
      window.alert(error);
      console.log(error);
  }
};

var BtnSave_cost = document.querySelector('#Btn_save_cost');
BtnSave_cost.addEventListener("click", insert_cost);


// this function is for displaying Cost Transaction 
    const  display_cost =  async () => {
      var datefrom = document.getElementById("datefrom_cost").value || ''
      var dateto = document.getElementById("dateto_cost").value || ''
      var equipmentID = document.getElementById("equipmentID_cost_search").value || ''
      
      const search_url = `/api-get-sgmc-cost-transaction/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;
  
  
      const responce = await fetch(search_url)
      const data = await responce.json();
      console.log(data)
  
      if (data.length === 0) {
              window.alert('No Data available');
          };
      
      
      if (responce.status === 200){
          let tableData="";
          let sum = 0;
          data.costData.map((values, index)=>{
              const columnNumber = index + 1; 
              
              tableData+= ` <tr>
                          <td>${columnNumber}</td>
                          <td>${values.id}</td>
                          <td>${values.transDate}</td>
                          <td>${values.equipment_id}</td>
                          <td>${values.cost_details}</td>
                          <td>${values.amount}</td>
                          <td>${values.particular}</td>
                         
                          
                          
                          <td>
                              <a href="/update-cost-sgmc/${values.id}"
                              <button type="button" class="btn btn-primary">
                              <i class="fas fa-database"></i> Edit</button></a> 
                      
                          </td>
                      
                      </tr>`;
          });
          document.getElementById("table_body_cost").innerHTML=tableData;
          document.getElementById('total_amount_cost').value = data.totalAmount
          // var test = 1000
          // document.getElementById("fter_totalBillinglTons").value = test;
          sumtoTalAmountDiesel()
      }else if (responce.status === 401){
          window.alert("Unauthorized Credentials Please Log in")
      }
  
  };
  
  
  var BtnSearch_cost = document.querySelector('#BtnSearch_cost');
  BtnSearch_cost.addEventListener("click", display_cost);
  





  




    


