//=======================================This is for Next Nad Back Function for Page=============================


// let currentPage = 1;
// const totalPages = 2;
// const nextPage = () => {
//   if (currentPage === 1) {
//     const inputs = document.querySelectorAll('#page1 input');
//     let isFilled = true;
//     inputs.forEach((input) => {
//       if (input.value === '') {
//         isFilled = false;
//         return;
//       }
//     });

//     if (isFilled) {
//       currentPage++;
//       const currentPageElem = document.getElementById('page' + currentPage);
//       currentPageElem.style.display = 'block';

//       const previousPageElem = document.getElementById('page' + (currentPage - 1));
//       previousPageElem.style.display = 'none';

     
//     } else {
//       alert('Please fill in all the fields before proceeding.');
//     }
//   } else if (currentPage === 2) {
//     const inputs = document.querySelectorAll('#page2 input');
//     let isFilled = true;
//     inputs.forEach((input) => {
//       if (input.value === '') {
//         isFilled = false;
//         return;
//       }
//     });

//     if (isFilled) {
//       alert('All fields are filled. Proceed to the next step.');
//     } else {
//       alert('Please fill in all the fields before proceeding.');
//     }
//   }
// };

// const previousPage = () => {
//   currentPage--;
//   const currentPageElem = document.getElementById('page' + currentPage);
//   currentPageElem.style.display = 'block';

//   const nextPageElem = document.getElementById('page' + (currentPage + 1));
//   nextPageElem.style.display = 'none';

  
// };

// // Attach the event listener to the button for Next Page
// const nextPageButton = document.querySelector('#nextPage');
// nextPageButton.addEventListener("click", nextPage);


// // Attach the event listener to the button for Next Page
// const previousPageButton = document.querySelector('#previousPage');
// previousPageButton.addEventListener("click", previousPage);

let currentPage = 1;
const totalPages = 3;

const nextPage = () => {
  if (currentPage < totalPages) {
    const inputs = document.querySelectorAll('#page' + currentPage + ' input');
    let isFilled = true;
    inputs.forEach((input) => {
      if (input.value === '') {
        isFilled = false;
        return;
      }
    });

    if (isFilled) {
      currentPage++;
      const currentPageElem = document.getElementById('page' + currentPage);
      currentPageElem.style.display = 'block';

      const previousPageElem = document.getElementById('page' + (currentPage - 1));
      previousPageElem.style.display = 'none';

      if (currentPage === totalPages) {
        nextPageButton.style.display = 'none';
      }
    } else {
      alert('Please fill in all the fields before proceeding.');
    }
  } else if (currentPage === totalPages) {
    const inputs = document.querySelectorAll('#page' + currentPage + ' input');
    let isFilled = true;
    inputs.forEach((input) => {
      if (input.value === '') {
        isFilled = false;
        return;
      }
    });

    if (isFilled) {
      alert('All fields are filled. Proceed to the next step.');
    } else {
      alert('Please fill in all the fields before proceeding.');
    }
  }
};

const previousPage = () => {
  if (currentPage > 1) {
    currentPage--;
    const currentPageElem = document.getElementById('page' + currentPage);
    currentPageElem.style.display = 'block';

    const nextPageElem = document.getElementById('page' + (currentPage + 1));
    nextPageElem.style.display = 'none';

    nextPageButton.style.display = 'block';
  }
};

// Attach the event listener to the button for Next Page on page 1
const nextPageButton = document.querySelector('#nextPage');
nextPageButton.addEventListener('click', nextPage);

// Attach the event listener to the button for Next Page on page 2
const nextPageButton2 = document.querySelector('#nextPage2');
nextPageButton2.addEventListener('click', nextPage);

// Attach the event listener to the button for Previous Page
const previousPageButton = document.querySelector('#previousPage');
previousPageButton.addEventListener('click', previousPage);

// Attach the event listener to the button for Previous Page
const previousPageButton2 = document.querySelector('#previousPage2');
previousPageButton2.addEventListener('click', previousPage);

// =================================================This is for selection of Employee  ID ==============================
$(document).ready(function() {
    $("#employee_id").on("keyup", async function(event) {
        // check if Enter key was pressed
        if (event.keyCode === 13 || event.keyCode === 9) {
        // trigger button click event
            var employee_id = $("#employee_id").val()

            const search_url = `/api-search-employee_by_empID/?term=${employee_id}`;


            const responce =  await fetch(search_url)
            const data =  await responce.json();
            console.log(data)
            

            if (data.length === 0){
                window.alert(`No ID store for ${employee_id}`)
            } else if (responce.status == 401){
                window.alert("Unauthorized Please Login")

            }else{
            
                var name = data[0].firstName
                var lname = data[0].lastName
                var position = data[0].position
                var salary_rate = data[0].salary_rate
                var taxCode = data[0].taxCode
                var off_on_details = data[0].off_on_details
                var salary_details = data[0].Salary_Detail
                var department = data[0].department

                $('#fname').val(name)
                $('#lname').val(lname)
                $('#position').val(position)
                $('#salary_rate').val(salary_rate)
                $('#tax_class').val(taxCode)
                $('#emp_class').val(off_on_details)
                $('#salary_details').val(salary_details)
                $('#department').val(department)

                

                if (employee_id <= 2021) {
                        provi_rate = 570
                        $('#provi_rate').val(provi_rate)
                        
                    }else if(employee_id >= 2022 && employee_id <=2999){
                        provi_rate = 429
                        $('#provi_rate').val(provi_rate)
                    }else if (employee_id >= 5000 && employee_id <=7000){
                        provi_rate = 351
                        $('#provi_rate').val(provi_rate)
                    } else {
                        provi_rate = 429
                        $('#provi_rate').val(provi_rate)
                    }
                

            }
    
        }
    });
});  

// =================================================This is for calculation of Regday=======================================
// Get the elements we need
                const regdayInput = document.getElementById('regday');
                const salaryDetails = document.getElementById('salary_details');
                const salaryRateInput = document.getElementById('salary_rate');
                const salaryRateInputAdan = document.getElementById('salary_rate_Adan');
                const regdayCalInput = document.getElementById('regday_cal');

                // Add an event listener to the regday input to calculate the regular day calculation
                // when the value of the input changes
                regdayInput.addEventListener('input', function(e) {
                    // Get the values from the inputs
                    const regday = Number(e.target.value);
                    const salaryDetailsValue = salaryDetails.value;
                    //.1675213
                    let salaryRate = Number(salaryRateInputAdan.value);

                    // Calculate the salary rate and regular day calculation
                    const regularDayCalculation = calculateRegularDay(
                    salaryDetailsValue,
                    salaryRate,
                    regday
                    );

                    // Update the regular day calculation input with the result
                    regdayCalInput.value = regularDayCalculation.toFixed(2);
                    calculatetotalGross()
                });

                // Function to calculate the regular day calculation
                function calculateRegularDay(salaryDetails, salaryRate, regularDay) {
                    // If the salary is monthly, divide the salary rate by 26 to get the daily rate
                    if (salaryDetails === 'Monthly') {
                    salaryRate = salaryRate / 26;
                    }

                    // Return the regular day calculation
                    return salaryRate * regularDay;
                    
                }

// ==================================This is for Reg Day OY ==========================================

            document.getElementById('regday_ot').addEventListener('input',
            function(e){
                let regday_ot = e.target.value;

                var salDetails = document.getElementById('salary_details').value;
                var salaryRate;
                var regday_otCal;

                if (salDetails == 'Monthly'){
                    salaryRate =  document.getElementById('salary_rate').value / 26;
                    regday_otCal = parseFloat(salaryRate) / 8 * 1.25 * parseFloat(regday_ot)
                    document.getElementById('regday_ot_cal').value=regday_otCal.toFixed(2);
                    calculatetotalGross()
                }else{
                    salaryRate =  document.getElementById('salary_rate').value ;
                    regday_otCal = parseFloat(salaryRate) / 8 * 1.25 * parseFloat(regday_ot)
                    document.getElementById('regday_ot_cal').value=regday_otCal.toFixed(2);
                    calculatetotalGross()

                }
   
            }
            );

// ======================================This is for Sunday ==========================================
            document.getElementById('sunday').addEventListener('input',
            function(e){
                let sundayReg = e.target.value;
                var salDetails = document.getElementById('salary_details').value;
                
                var salaryRate;
                
                var sundayReg_cal;

                if (salDetails == 'Monthly'){
                    salaryRate =  document.getElementById('salary_rate').value / 26;
                    sundayReg_cal = parseFloat(salaryRate) * parseFloat(sundayReg) * 1.30
                    document.getElementById('sunday_cal').value=sundayReg_cal.toFixed(2);
                    calculatetotalGross()
                }else{
                    salaryRate =  document.getElementById('salary_rate').value;
                    sundayReg_cal = parseFloat(salaryRate) * parseFloat(sundayReg) * 1.30
                    document.getElementById('sunday_cal').value=sundayReg_cal.toFixed(2);
                    calculatetotalGross()
                }
                
                
                
            }
            );

// =================================This is for Sunday OT Calculation============================ 
            
                document.getElementById('sunday_ot').addEventListener('input',
                function(e){
                    let sunday_ot = e.target.value;
    
                    var salDetails = document.getElementById('salary_details').value;
                    var salaryRate;
                    var sunday_otCal;
    
                    if (salDetails == 'Monthly'){
                        salaryRate =  document.getElementById('salary_rate').value / 26;
                        sunday_otCal = parseFloat(salaryRate) / 8 * 1.69 * parseFloat(sunday_ot)
                        document.getElementById('sunday_ot_cal').value=sunday_otCal.toFixed(2);
                        calculatetotalGross()
                    }else{
                        salaryRate =  document.getElementById('salary_rate').value ;
                        sunday_otCal = parseFloat(salaryRate) / 8 * 1.69 * parseFloat(sunday_ot)
                        document.getElementById('sunday_ot_cal').value=sunday_otCal.toFixed(2);
                        calculatetotalGross()
                    }
    
                }
                );
    
// -- =================================This is for SPL Calculation============================ -->
              
                    document.getElementById('spl').addEventListener('input',
                    function(e){
                        let spl = e.target.value;
        
                        var salDetails = document.getElementById('salary_details').value;
                        var salaryRate;
                        var spl_cal;
        
                        if (salDetails == 'Monthly'){
                            salaryRate =  document.getElementById('salary_rate').value / 26;
                            spl_cal = parseFloat(salaryRate) * parseFloat(spl) * 1.30
                            document.getElementById('spl_cal').value=spl_cal.toFixed(2);
                            calculatetotalGross()
                        }else{
                            salaryRate =  document.getElementById('salary_rate').value ;
                            spl_cal = parseFloat(salaryRate) * parseFloat(spl) * 1.30
                            document.getElementById('spl_cal').value=spl_cal.toFixed(2);
                            calculatetotalGross()
                        }
        
                    }
                    );
        
// - =================================This is for SPL OT  Calculation============================ -->
                    
                        document.getElementById('spl_ot').addEventListener('input',
                        function(e){
                            let spl_ot = e.target.value;
            
                            var salDetails = document.getElementById('salary_details').value;
                            var salaryRate;
                            var spl_ot_cal;
            
                            if (salDetails == 'Monthly'){
                                salaryRate =  document.getElementById('salary_rate').value / 26;
                                spl_ot_cal = parseFloat(salaryRate) / 8 * 1.69 * parseFloat(spl_ot)
                                document.getElementById('spl_ot_cal').value=spl_ot_cal.toFixed(2);
                                calculatetotalGross()
                            }else{
                                salaryRate =  document.getElementById('salary_rate').value ;
                                spl_ot_cal = parseFloat(salaryRate)/ 8 * 1.69 * parseFloat(spl_ot) 
                                document.getElementById('spl_ot_cal').value=spl_ot_cal.toFixed(2);
                                calculatetotalGross()
                            }
            
                        }
                        );
            
// -- =================================This is for LGL2 Calculation============================ -->
                       
                            document.getElementById('lgl2').addEventListener('input',
                            function(e){
                                let spl = e.target.value;
                
                                var salDetails = document.getElementById('salary_details').value;
                                var salaryRate;
                                var lgl2_cal;
                
                                if (salDetails == 'Monthly'){
                                    salaryRate =  document.getElementById('salary_rate').value / 26;
                                    lgl2_cal = parseFloat(salaryRate) * parseFloat(spl) * 2
                                    document.getElementById('lgl2_cal').value=lgl2_cal.toFixed(2);
                                    calculatetotalGross()
                                }else{
                                    salaryRate =  document.getElementById('salary_rate').value ;
                                    lgl2_cal = parseFloat(salaryRate) * parseFloat(spl) * 2
                                    document.getElementById('lgl2_cal').value=lgl2_cal.toFixed(2);
                                    calculatetotalGross()
                
                                }
                
                            }
                            );
                
// -- =================================This is for LGL2 OT  Calculation============================ -->
                           
                               
                                 // Get the elements we need
                                    const lgl2OvertimeInput = document.getElementById('lgl2_ot');
                                    const salaryDetails2 = document.getElementById('salary_details');
                                    const salaryRateInput2= document.getElementById('salary_rate');
                                    const lgl2OvertimeCalculationInput = document.getElementById('lgl2_ot_cal');
                    
                                    // Add an event listener to the lgl2 overtime input to calculate the overtime calculation
                                    // when the value of the input changes
                                    lgl2OvertimeInput.addEventListener('input', function(e) {
                                        // Get the values from the inputs
                                        const lgl2Overtime = Number(e.target.value);
                                        const salaryDetailsValue = salaryDetails2.value;
                                        const salaryRate = Number(salaryRateInput2.value);
                    
                                        // Calculate the overtime calculation
                                        const lgl2OvertimeCalculation = calculateOvertime(
                                        salaryDetailsValue,
                                        salaryRate,
                                        lgl2Overtime
                                        );
                    
                                        // Update the overtime calculation input with the result
                                        lgl2OvertimeCalculationInput.value = lgl2OvertimeCalculation.toFixed(2);
                                        calculatetotalGross()
                                    });
                    
                                    // Function to calculate the overtime calculation
                                    function calculateOvertime(salaryDetails2, salaryRate, lgl2Overtime) {
                                        // If the salary is monthly, divide the salary rate by 26 to get the daily rate
                                        if (salaryDetails2 === 'Monthly') {
                                        salaryRate = salaryRate / 26;
                                        }
                    
                                        // Return the overtime calculation
                                        return salaryRate / 8 * 2 * 1.30 * lgl2Overtime;
                                    }
                    
                           
                    
                    
// // -- ====================================This is for computation of ShopRate==================================== -->
                           
//                                  $(document).ready(function() {
//                                     $('#shoprate, #salary_rate').on('input', function() {
//                                         calculateProductShopRate();
//                                     });
//                                     });
                    
//                                     function calculateProductShopRate() {
//                                     let product;
//                                     let salaryDetails = $('#salary_details').val();
                                    
//                                     var salaryRate = $('#salary_rate').val();
//                                     var shoprate = $('#shoprate').val();
                    
//                                     if (salaryDetails  === 'Monthly'){
//                                         salaryRate = salaryRate / 26;
//                                         product = salaryRate / 2 * shoprate;
//                                         product = product.toFixed(2)
//                                         $('#shopRate_cal').val(product);
//                                         calculatetotalGross()
                    
//                                     }
//                                     product = salaryRate / 2 * shoprate;
//                                     product = product.toFixed(2)
//                                         $('#shopRate_cal').val(product);
//                                         calculatetotalGross()
//                                     }
                    
                    
                           
                    
// //  ====================================This is for computation of ProviRate Calcuation==================================== -->
                               
//                                     $(document).ready(function() {
//                                     $('#provirateNo, #provi_rate').on('input', function() {
//                                         calculateProvi();
//                                     });
//                                     });
                    
//                                     function calculateProvi() {
//                                     let product
//                                     var totalProvi = $('#provirateNo').val();
//                                     var proviRate = $('#provi_rate').val();
                                    
//                                     product = totalProvi  * proviRate;
//                                     product = product.toFixed(2)
//                                     $('#provirate_cal').val(product);
//                                     calculatetotalGross()
//                                     }
                    
                    
                                
                    
// // ====================================This is for computation of ProviRate Calcuation==================================== -->
                                    
//                                         $(document).ready(function() {
//                                         $('#proviOT_total, #provi_rate').on('input', function() {
//                                             calculateProviOT();
//                                         });
//                                         });
                    
//                                         function calculateProviOT() {
//                                         let product
//                                         var totalProvi = $('#proviOT_total').val();
//                                         var proviRate = $('#provi_rate').val();
                                        
//                                         product = totalProvi  * ((proviRate) / 8 * 1.25);
//                                         product = product.toFixed(2);
//                                         $('#proviOT_total_cal').val(product);
//                                         calculatetotalGross()
//                                         }
                    
                    
                                    
                    
// // <!-- ====================================This is for computation of ProviRate Calcuation==================================== -->
                                    
//                                         $(document).ready(function() {
//                                         $('#provisun_total, #provi_rate').on('input', function() {
//                                             calculateProviSun();
//                                         });
//                                         });
                    
//                                         function calculateProviSun() {
//                                         let product
//                                         var totalProvi = $('#provisun_total').val();
//                                         var proviRate = $('#provi_rate').val();
                                        
//                                         product = totalProvi  * (proviRate * 1.30);
//                                         product = product.toFixed(2)
//                                         $('#provisun_total_cal').val(product);
//                                         calculatetotalGross()
//                                         }
                    
                    
                                    
                    
                    
// // <!-- ====================================This is for computation of Provi Sun OT Cal==================================== -->
                                    
//                                         $(document).ready(function() {
//                                         $('#provisunOT_total, #provi_rate').on('input', function() {
//                                             calculateProviSunOT();
//                                         });
//                                         });
                    
//                                         function calculateProviSunOT() {
//                                         let product
//                                         var totalProvi = $('#provisunOT_total').val();
//                                         var proviRate = $('#provi_rate').val();
                                        
//                                         product = totalProvi  * ((proviRate)/8 * 1.69);
//                                         product = product.toFixed(2)
//                                         $('#provisunOT_total_cal').val(product);
//                                         calculatetotalGross()
//                                         }
                    
                    
                                    
                    
// <!-- ====================================This is for computation of Regday  Night diff ==================================== -->
                                    
                                        $(document).ready(function() {
                                        $('#nightDiff, #salary_rate_Adan').on('input', function() {
                                            calculateNightDiff();
                                        });
                                        });
                    
                                        function calculateNightDiff() {
                                        let product
                                        var nightDiff = $('#nightDiff').val();
                                        var salaryRate = $('#salary_rate_Adan').val();
                                        
                                        product = nightDiff  * ((salaryRate)/8 * 0.10);
                                        product = product.toFixed(2)
                                        $('#nightDiff_cal').val(product);
                                        calculatetotalGross()
                                        }

// <!-- ====================================This is for computation of Regday OT  Night diff ==================================== -->
                                    
                                        $(document).ready(function() {
                                        $('#nightDiff_regday_ot, #salary_rate').on('input', function() {
                                            calculateNightDiff_ot();
                                        });
                                        });
                    
                                        function calculateNightDiff_ot() {
                                        let product
                                        var nightDiff = $('#nightDiff_regday_ot').val();
                                        var salaryRate = $('#salary_rate').val();
                                        
                                        product = nightDiff  * ((salaryRate)/8 * 1.25 * 0.10);
                                        product = product.toFixed(2)
                                        $('#nightDiff_regdayOT_cal').val(product);
                                        calculatetotalGross()
                                        }
// <!-- ====================================This is for computation of SPL/RestDay  Night diff ==================================== -->
                                    
                                        $(document).ready(function() {
                                        $('#nightDiff_spl, #salary_rate').on('input', function() {
                                            calculateNightDiff_spl();
                                        });
                                        });
                    
                                        function calculateNightDiff_spl() {
                                        let product
                                        var nightDiff = $('#nightDiff_spl').val();
                                        var salaryRate = $('#salary_rate').val();
                                        
                                        product = nightDiff  * ((salaryRate)/8 * 1.30 * 0.10);
                                        product = product.toFixed(2)
                                        $('#nightDiff_spl_cal').val(product);
                                        calculatetotalGross()
                                        }


// <!-- ====================================This is for computation of SPL/RestDay OT  Night diff ==================================== -->
                                    
                                $(document).ready(function() {
                                    $('#nightDiff_spl_ot, #salary_rate').on('input', function() {
                                        calculateNightDiff_spl_ot();
                                    });
                                    });

                                    function calculateNightDiff_spl_ot() {
                                    let product
                                    var nightDiff = $('#nightDiff_spl_ot').val();
                                    var salaryRate = $('#salary_rate').val();
                                    
                                    product = nightDiff  * ((salaryRate)/8 * 1.69 * 0.10);
                                    product = product.toFixed(2)
                                    $('#nightDiff_splOT_cal').val(product);
                                    calculatetotalGross()
                                    }


// <!-- ==============================This is for computation of Legal Holiday  Night diff ==================================== -->
                                    
                                $(document).ready(function() {
                                    $('#nightDiff_lgl2, #salary_rate').on('input', function() {
                                        calculateNightDiff_lgl2();
                                    });
                                    });

                                    function calculateNightDiff_lgl2() {
                                    let product
                                    var nightDiff = $('#nightDiff_lgl2').val();
                                    var salaryRate = $('#salary_rate').val();
                                    
                                    product = nightDiff  * ((salaryRate)/8 * 2 * 0.10);
                                    product = product.toFixed(2)
                                    $('#nightDiff_lgl2_cal').val(product);
                                    calculatetotalGross()
                                    }

// <!-- ==============================This is for computation of Legal Holiday OT  Night diff ==================================== -->
                                    
                                // $(document).ready(function() {
                                //     $('#nightDiff_lgl2_ot, #salary_rate').on('input', function() {
                                //         calculateNightDiff_lgl2_ot();
                                //     });
                                //     });

                                //     function calculateNightDiff_lgl2_ot() {
                                //     let product
                                //     var nightDiff = $('#nightDiff_lgl2_ot').val();
                                //     var salaryRate = $('#salary_rate').val();
                                    
                                //     product = nightDiff  * parseFloat(salaryRate)/8 * (2) *  (1.25) * (0.10);
                                //     product = product.toFixed(2)
                                //     $('#nightDiff_lgl2OT_cal').val(product);
                                //     calculatetotalGross()
                                //     }
                                // //     //This is for error 6.26.2023 5:37 PM"
                                // //     //another try
                                   
                    
// <!-- ====================================This is for computation of Total Gross==================================== -->
                                   
                                        // $(document).ready(function() {
                                        //     $('#regday_cal, #regday_ot_cal, \
                                        //     #sunday_cal,#sunday_ot_cal,#spl_cal, \
                                        //     #spl_ot_cal,#lgl2_cal,#lgl2_ot_cal, \
                                        //     #nightDiff_cal,#nightDiff_regdayOT_cal, \
                                        //     #nightDiff_spl_cal,#nightDiff_splOT_cal,\
                                        //     #nightDiff_lgl2_cal,#nightDiff_lgl2OT_cal,\
                                        //     #adjustment').on('input', function() {
                                        //         calculatetotalGross();
                                        //     });
                                        //     });
                    
                                        //     function calculatetotalGross() {
                                            
                                        //     let regdayCal;
                                        //     let regdayOTCal;
                                        //     let sunday_cal;
                                        //     let sunday_ot_cal;
                                        //     let spl_cal;
                                        //     let spl_ot_cal;
                                        //     let lgl2_cal;
                                        //     let lgl2_ot_cal;
                                        //     let nightDiff_cal;
                                        //     let nightDiff_regdayOT_cal;
                                        //     let nightDiff_spl_cal;
                                        //     let nightDiff_splOT_cal;
                                        //     let nightDiff_lgl2_cal;
                                        //     let nightDiff_lgl2OT_cal;
                                        //     let adjustment;
                    
                    
                                        //     regdayCal = $('#regday_cal').val() || 0;
                                        //     regdayOTCal = $('#regday_ot_cal').val() || 0;
                                        //     sunday_cal = $('#sunday_cal').val() || 0;
                                        //     sunday_ot_cal = $('#sunday_ot_cal').val() || 0;
                                        //     spl_cal = $('#spl_cal').val() || 0;
                                        //     spl_ot_cal = $('#spl_ot_cal').val() || 0;
                                        //     lgl2_cal = $('#lgl2_cal').val() || 0;
                                        //     lgl2_ot_cal = $('#lgl2_ot_cal').val() || 0;
                                        //     nightDiff_cal = $('#nightDiff_cal').val() || 0;
                                        //     nightDiff_regdayOT_cal = $('#nightDiff_regdayOT_cal').val() || 0;
                                        //     nightDiff_spl_cal = $('#nightDiff_spl_cal').val() || 0;
                                        //     nightDiff_splOT_cal = $('#nightDiff_splOT_cal').val() || 0;
                                        //     nightDiff_lgl2_cal = $('#nightDiff_lgl2_cal').val() || 0;
                                        //     nightDiff_lgl2OT_cal = $('#nightDiff_lgl2OT_cal').val() || 0;
                                        //     adjustment = $('#adjustment').val() || 0;
                                            
                                        //     let product;
                                        //     let product2
                                        //     product = (parseFloat(regdayCal) + parseFloat(regdayOTCal)
                                        //                     + parseFloat(sunday_cal) + parseFloat(sunday_ot_cal)
                                        //                     + parseFloat(spl_cal) + parseFloat(spl_ot_cal)
                                        //                     + parseFloat(lgl2_cal) + parseFloat(lgl2_ot_cal)
                                        //                     + parseFloat(nightDiff_cal) + parseFloat(nightDiff_regdayOT_cal)
                                        //                     + parseFloat(nightDiff_spl_cal) + parseFloat(nightDiff_splOT_cal)
                                        //                     + parseFloat(nightDiff_lgl2_cal) + parseFloat(nightDiff_lgl2OT_cal)
                                        //                     + parseFloat(adjustment));
                    
                                        //     product2 = product.toFixed(2);
                                        //     const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                                        //     $('#totalGross').val(stringNumber);
                                        //     $('#totalGross2').val(product2);
                                        //     }
                    
                        // $(document).ready(function() {
                        //     $('#regday_cal, #regday_ot_cal, #sunday_cal, #sunday_ot_cal, #spl_cal, #spl_ot_cal, #lgl2_cal, #lgl2_ot_cal, #nightDiff_cal, #nightDiff_regdayOT_cal, #nightDiff_spl_cal, #nightDiff_splOT_cal, #nightDiff_lgl2_cal, #nightDiff_lgl2OT_cal, #adjustment,#totalGross').on('input', function() {
                        //         calculateTotalGross();
                        //     });
                        //     });
                            
                        //     function calculateTotalGross() {
                        //         let regdayCal = parseFloat($('#regday_cal').val()) || 0;
                        //         let regdayOTCal = parseFloat($('#regday_ot_cal').val()) || 0;
                        //         let sundayCal = parseFloat($('#sunday_cal').val()) || 0;
                        //         let sundayOTCal = parseFloat($('#sunday_ot_cal').val()) || 0;
                        //         let splCal = parseFloat($('#spl_cal').val()) || 0;
                        //         let splOTCal = parseFloat($('#spl_ot_cal').val()) || 0;
                        //         let lgl2Cal = parseFloat($('#lgl2_cal').val()) || 0;
                        //         let lgl2OTCal = parseFloat($('#lgl2_ot_cal').val()) || 0;
                        //         let nightDiffCal = parseFloat($('#nightDiff_cal').val()) || 0;
                        //         let nightDiffRegdayOTCal = parseFloat($('#nightDiff_regdayOT_cal').val()) || 0;
                        //         let nightDiffSplCal = parseFloat($('#nightDiff_spl_cal').val()) || 0;
                        //         let nightDiffSplOTCal = parseFloat($('#nightDiff_splOT_cal').val()) || 0;
                        //         let nightDiffLgl2Cal = parseFloat($('#nightDiff_lgl2_cal').val()) || 0;
                        //         let nightDiffLgl2OTCal = parseFloat($('#nightDiff_lgl2OT_cal').val()) || 0;
                        //         let adjustment = parseFloat($('#adjustment').val()) || 0;
                              
                        //         let totalGross = regdayCal + regdayOTCal + sundayCal + sundayOTCal + splCal + splOTCal + lgl2Cal + lgl2OTCal + nightDiffCal + nightDiffRegdayOTCal + nightDiffSplCal + nightDiffSplOTCal + nightDiffLgl2Cal + nightDiffLgl2OTCal + adjustment;
                                
                        //         let totalGrossFormatted = totalGross.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                                
                        //         $('#totalGross').val(totalGrossFormatted);
                        //         $('#totalGross2').val(totalGross.toFixed(2));
                        //       }
                                          
                                          
//===========================================This function is for inserting Payroll TVI====================================
const insertPayrollTVI = async() => {
    // Get the values of the input fields
    const salaryRateInput = document.getElementById('salary_rate');
    // let salaryRate = Number(salaryRateInput.value) + (Number(salaryRateInput.value) * .1675213);
    // let salaryRate = document.getElementById('salary_rate_Adan')
    // salaryRate = salaryRate.toFixed(2)
    const nightDiff_cal = document.getElementById("nightDiff_cal").value || 0
    const nightDiff_regdayOT_cal = document.getElementById("nightDiff_regdayOT_cal").value || 0
    const nightDiff_spl_cal = document.getElementById("nightDiff_spl_cal").value || 0
    const nightDiff_splOT_cal = document.getElementById("nightDiff_splOT_cal").value || 0

    const nightDiff_lgl2_cal = document.getElementById("nightDiff_lgl2_cal").value || 0
    const nightDiff_lgl2OT_cal = document.getElementById("nightDiff_lgl2OT_cal").value || 0

    let totalNightdiff = ( parseFloat(nightDiff_cal) + parseFloat(nightDiff_regdayOT_cal) 
                           + parseFloat(nightDiff_spl_cal) + parseFloat(nightDiff_splOT_cal) 
                           + parseFloat(nightDiff_lgl2_cal) + parseFloat(nightDiff_lgl2OT_cal)
                            )

    totalNightdiff = totalNightdiff.toFixed(2)

    const data = {
        transDate: document.getElementById("datefrom").value,
        employee_id: document.getElementById("employee_id").value,
        first_name: document.getElementById("fname").value,
        last_name: document.getElementById("lname").value,
        salaryRate: document.getElementById("salary_rate").value || 0,
        addOnRate: document.getElementById("salary_rate_Adan").value || 0,
        salaryDetails: document.getElementById("salary_details").value || 0,
        regDay: document.getElementById("regday").value || 0,
        regDayOt: document.getElementById("regday_ot").value || 0,
        sunday: document.getElementById("sunday").value || 0,
        sundayOT: document.getElementById("sunday_ot").value || 0,
        spl: document.getElementById("spl").value || 0,
        splOT: document.getElementById("spl_ot").value || 0,
        lgl2: document.getElementById("lgl2").value || 0,
        lgl2OT: document.getElementById("lgl2_ot").value || 0,
        nightDiff: totalNightdiff,
        adjustment: document.getElementById("adjustment").value || 0,


    };
    console.log(data);

    const inputs = document.querySelectorAll('#page2 input');
    let isFilled = true;
    inputs.forEach((input) => {
      if (input.value === '') {
        isFilled = false;
        return;
      }
    });

    const inputs1 = document.querySelectorAll('#page3 input');
    let isFilled1 = true;
    inputs1.forEach((input) => {
      if (input.value === '') {
        isFilled1 = false;
        return;
      }
    });

    if (isFilled) {
        try {
            const response = await fetch(`/api-insert-tvi-payroll/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            // Check if the response was successful
            if (response.status === 200) {
                window.alert("Your data has been saved");
                window.location.assign("/employee-transaction-tvi/");
            } else if (response.status === 401) {
                window.alert("Unauthorized credential. Please login");
            }
        } catch (error) {
            // Catch any errors and log them to the console
            window.alert(error);
            console.log(error);
        }
    } else {
      alert('Please fill in all the fields before proceeding.');
    }
    
       
    }

                                    
const BTN_saveTVI_Payroll = document.querySelector('#Btn_Save_payroll');
BTN_saveTVI_Payroll.addEventListener("click", insertPayrollTVI);                  
                    
                    
                                                                             
// =========================This function is for Displaying Data of Tons Transaction ============================
