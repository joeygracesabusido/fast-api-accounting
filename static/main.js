// ============================This is for function of Displaying Query for Employee================
$(document).ready(function() {
  $('#myCheckbox2').change(function() {
  if($(this).prop('checked')) {
     
      deminimis_computation()
      totalDeminimis()
      calculateOtherForms()
  }else{
    withoutDeminimis()
    totalDeminimis()
    calculateOtherForms()
  }
  });
});




// ==========================This is for calculation of Gross Payroll=============================
$(document).ready(function() {
    $('#regday_cal, #regday_ot_cal, \
    #sunday_cal,#sunday_ot_cal,#spl_cal, \
    #spl_ot_cal,#lgl2_cal,#lgl2_ot_cal, \
    #shopRate_cal,#provirate_cal,#proviOT_total_cal, \
    #provisun_total_cal,#provisunOT_total_cal,\
    #nightDiff_cal,#adjustment').on('input', function() {
        calculatetotalGross();
    });
    });

    function calculatetotalGross() {
    
    let regdayCal;
    let regdayOTCal;
    let sunday_cal;
    let sunday_ot_cal;
    let spl_cal;
    let spl_ot_cal;
    let lgl2_cal;
    let lgl2_ot_cal;
    let shopRate_cal;
    let provirate_cal;
    let proviOT_total_cal;
    let provisun_total_cal;
    let provisunOT_total_cal;
    let nightDiff_cal;
    let adjustment;


    regdayCal = $('#regday_cal').val();
    regdayOTCal = $('#regday_ot_cal').val();
    sunday_cal = $('#sunday_cal').val();
    sunday_ot_cal = $('#sunday_ot_cal').val();
    spl_cal = $('#spl_cal').val();
    spl_ot_cal = $('#spl_ot_cal').val();
    lgl2_cal = $('#lgl2_cal').val();
    lgl2_ot_cal = $('#lgl2_ot_cal').val();
    shopRate_cal = $('#shopRate_cal').val();
    provirate_cal = $('#provirate_cal').val();
    proviOT_total_cal = $('#proviOT_total_cal').val();
    provisun_total_cal = $('#provisun_total_cal').val();
    provisunOT_total_cal = $('#provisunOT_total_cal').val();
    nightDiff_cal = $('#nightDiff_cal').val();
    adjustment = $('#adjustment').val();
    
    let product;
    let product2
    product = (parseFloat(regdayCal) + parseFloat(regdayOTCal)
                     + parseFloat(sunday_cal) + parseFloat(sunday_ot_cal)
                     + parseFloat(spl_cal) + parseFloat(spl_ot_cal)
                     + parseFloat(lgl2_cal) + parseFloat(lgl2_ot_cal)
                     + parseFloat(shopRate_cal) + parseFloat(provirate_cal) + parseFloat(proviOT_total_cal)
                     + parseFloat(provisun_total_cal) + parseFloat(provisunOT_total_cal)
                     + parseFloat(nightDiff_cal) + parseFloat(adjustment));

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#totalGross').val(stringNumber);
    $('#totalGross2').val(product2);
    }


// This function is for for Gov't Mandatory

$(document).ready(function() {
    $('#myCheckbox').change(function() {
      if($(this).prop('checked')) {

     
        let sss;
        let phic;
        let hdmf;
        let sssProv;
        
        display_sss_data()
        calculateTotalGov()
        
 
      } else {
        let sss;
        let phic;
        let hdmf;
        let sssProv;
        let totalGov;

        sss = 0.00
        phic = 0.00
        hdmf = 0.00
        sssProv = 0.00
        $('#sss').val(sss);
        $('#phic').val(phic);
        $('#hdmf').val(hdmf);
        $('#sssProv').val(sssProv);

        totalGov = sss + phic + hdmf + sssProv
        $('#totalGov').val(totalGov);
        calculateTotalGov()
      }
    });
  });


 
  
// This is for compuation of SSS
const display_sss_data = async () => {
  let grossSalary;
  let sssAmount;
  let salary_details;
  let salary_rate;
  let phic;
  let hdmf;
  let sssProv;

  salary_details = $('#salary_details').val();
  salary_rate = $('#salary_rate').val();

  if (salary_details == 'Monthly') {
    salary_rate = salary_rate;
  } else {
    salary_rate = salary_rate * 26;
  }

  const search_url = `/sss-computation/`;

  const response = await fetch(search_url);
  const data = await response.json();

  if (response.status === 401) {
    window.alert("Unauthorized credential. Please login");
    } else {
      for (let i of data) {
        if (i.amountTo >= salary_rate && i.amountFrom <= salary_rate) {
          sssAmount = i.empShare;
          sssAmount = sssAmount.toFixed(2);
          $('#sss').val(sssAmount);
          calculateTotalGov();
        }
      }
    }

  

  if (salary_rate <= 10000) {
    phic = 400 / 2;
    phic = phic.toFixed(2);
    $('#phic').val(phic);
    calculateTotalGov();
  } else if (salary_rate > 10000 && salary_rate < 80000) {
    phic = salary_rate * 0.04 / 2;
    phic = phic.toFixed(2);
    $('#phic').val(phic);
    calculateTotalGov();
  } else if (salary_rate >= 80000) {
    phic = 3200;
    phic = phic.toFixed(2);
    $('#phic').val(phic);
    calculateTotalGov();
  }

  hdmf = 100;
  $('#hdmf').val(hdmf);
  calculateTotalGov();

  sssProv = $('#sssProv').val();

  if (sssProv == '') {
    sssProv = 0.00;
    $('#sssProv').val(sssProv);
    calculateTotalGov();
  }
}



// const display_sss_data = async () => {
//     let grossSalary;
//     let sssAmount;
//     let salary_details;
//     let salary_rate;
//     let phic;
//     let hdmf;
//     let sssProv;
    

//     salary_details = document.getElementById('salary_details').value;
//     salary_rate = document.getElementById('salary_rate').value

//     if (salary_details == 'Monthly'){
//         salary_rate = salary_rate
//     }else{
//         salary_rate = salary_rate * 26
//     }
    
//     const search_url = `/sss-computation/`;

//     const responce = await fetch(search_url)
//     const data = await responce.json();

//     for (let i of data){
//         if (i.amountTo >= salary_rate && i.amountFrom <= salary_rate){
//             sssAmount = i.empShare
//             sssAmount = sssAmount.toFixed(2)
//             document.getElementById('sss').value = sssAmount
//             calculateTotalGov()
//         }

//     }

//     if (salary_rate <= 10000){
//         phic = 400 /2
//         phic = phic.toFixed(2)
//         document.getElementById('phic').value = phic
//         calculateTotalGov()

//     }else if(salary_rate > 10000){
//         phic = salary_rate * 0.04 / 2
//         phic = phic.toFixed(2)
//         document.getElementById('phic').value = phic
//         calculateTotalGov()
//     }else if(salary_rate >= 80000){
//         phic = 3200
//         phic = phic.toFixed(2)
//         document.getElementById('phic').value = phic
//         calculateTotalGov()

//     }
//     hdmf = 100
//     document.getElementById('hdmf').value = hdmf
//     calculateTotalGov()


//     sssProv = document.getElementById('sssProv').value;

//     if (sssProv == ''){
//         sssProv = 0.00
//         document.getElementById('sssProv').value = sssProv;
//         calculateTotalGov()


//     }
    
    // console.log(data.length)
      
// };

// This is for compuation of Total Mandatory
const sssInput = document.getElementById('sss');
const phicInput = document.getElementById('phic');
const hdmfInput = document.getElementById('hdmf');
const sssProvInput = document.getElementById('sssProv');
const totalGovOutput = document.getElementById('totalGov');

const calculateTotalGov = () => {
  const sss = parseFloat(sssInput.value);
  const phic = parseFloat(phicInput.value);
  const hdmf = parseFloat(hdmfInput.value);
  const sssProv = parseFloat(sssProvInput.value);
  let totalGov = parseFloat(sss) + parseFloat(phic) + parseFloat(hdmf) +  parseFloat(sssProv);
//   totalGov = totalGov.toFixed(2);

  totalGovOutput.value = totalGov;
}

sssInput.addEventListener('input', calculateTotalGov);
phicInput.addEventListener('input', calculateTotalGov);
hdmfInput.addEventListener('input', calculateTotalGov);
sssProvInput.addEventListener('input', calculateTotalGov);


//This is for computation of Deminimis


const deminimis_computation = async () => {

  
  let on_off_status;
  let totalGross2;
  let basic_taxable;
  let MWE = 3883.34/2;
  let basicMWE;
  let uniform;
  let rice;
  let laundry;
  let medical1;
  let medical2;

  on_off_status = document.getElementById('emp_class').value
  totalGross2 = document.getElementById('totalGross2').value
  basicMWE = (document.getElementById('provi_rate').value) * 13
  basic_taxable = totalGross2 - basicMWE 
  basic_taxable = basic_taxable.toFixed(2)
  console.log(basic_taxable)
  if (on_off_status == 'off'){
      uniform = 0
      uniform =uniform.toFixed(2)
      document.getElementById('uniform').value = uniform;

      rice = 0
      rice = rice.toFixed(2)
      document.getElementById('rice').value = rice;

      laundry = 0
      laundry = laundry.toFixed(2)
      document.getElementById('laundry').value = laundry;

      medical1 = 0
      medical1 = medical1.toFixed(2)
      document.getElementById('medical1').value = medical1;


      medical2 = 0
      medical2 = medical2.toFixed(2)
      document.getElementById('medical2').value = medical2;
      // totalDeminimis()

  }else if(basic_taxable > 0 && on_off_status == 'on' && basic_taxable >= MWE){
      uniform = MWE * 0.13
      uniform =uniform.toFixed(2)
      document.getElementById('uniform').value = uniform;

      rice = MWE * 0.52
      rice = rice.toFixed(2)
      document.getElementById('rice').value = rice;

      laundry = MWE * 0.08
      laundry = laundry.toFixed(2)
      document.getElementById('laundry').value = laundry;

      medical1 = MWE * 0.21
      medical1 = medical1.toFixed(2)
      document.getElementById('medical1').value = medical1;


      medical2 = MWE * 0.06
      medical2 = medical2.toFixed(2)
      document.getElementById('medical2').value = medical2;
      // totalDeminimis()
  }else if(basic_taxable > 0 && on_off_status == 'on' && basic_taxable <= MWE){
    uniform = basic_taxable * 0.13
    uniform =uniform.toFixed(2)
    document.getElementById('uniform').value = uniform;

    rice = basic_taxable * 0.52
    rice = rice.toFixed(2)
    document.getElementById('rice').value = rice;

    laundry = basic_taxable * 0.08
    laundry = laundry.toFixed(2)
    document.getElementById('laundry').value = laundry;

    medical1 = basic_taxable * 0.21
    medical1 = medical1.toFixed(2)
    document.getElementById('medical1').value = medical1;


    medical2 = basic_taxable * 0.06
    medical2 = medical2.toFixed(2)
    document.getElementById('medical2').value = medical2;
    // totalDeminimis()
}
  }

  const withoutDeminimis = async () =>{
    let rice;
    let laundry;
    let medical1;
    let medical2;
   
    uniform = 0
    uniform =uniform.toFixed(2)
    document.getElementById('uniform').value = uniform;

    rice = 0
    rice = rice.toFixed(2)
    document.getElementById('rice').value = rice;

    laundry = 0
    laundry = laundry.toFixed(2)
    document.getElementById('laundry').value = laundry;

    medical1 = 0
    medical1 = medical1.toFixed(2)
    document.getElementById('medical1').value = medical1;


    medical2 = 0
    medical2 = medical2.toFixed(2)
    document.getElementById('medical2').value = medical2;
    // totalDeminimis()
  }

const totalDeminimis = async () => {
  let rice;
  let uniform;
  let laundry;
  let medical1;
  let medical2;
  let totalDems;

  rice = $('#rice').val()
  uniform = $('#uniform').val()
  laundry = $('#laundry').val()
  medical1 = $('#medical1').val()
  medical2 = $('#medical2').val()


  totalDems =  parseFloat(uniform) +  parseFloat(rice) + parseFloat(laundry) + parseFloat(medical1) + parseFloat(medical2)
  totalDems = totalDems.toFixed(2);
  console.log(totalDems)
  $('#totalDeminimis').val(totalDems);
}

const calculateOtherForms = async () => {
  let allowance = document.querySelector('#allowance').value;
  let totalDeminimis = document.querySelector('#totalDeminimis').value;
  let salary_details = document.querySelector('#salary_details').value;
  let salary_rate = document.querySelector('#salary_rate').value;
  let provi_rate = document.querySelector('#provi_rate').value;
  let emp_class = document.querySelector('#emp_class').value;
  // let mweMonthly = parseFloat(provi_rate) * 13
  let salRate_allowance;
  let CalotherForms;
  
  

  totalGross2 = document.getElementById('totalGross2').value
  basicMWE = (document.getElementById('provi_rate').value) * 13
  basic_taxable = totalGross2 - basicMWE 
  basic_taxable = basic_taxable.toFixed(2)
 

  let afterDem = 0.00;
  let otherForms = 0.00;

  if (basic_taxable !== '0.00'){
    afterDem = (basic_taxable - totalDeminimis);

  }

  

  // This is for Determining if salary is monthly or to get the Total salary for 15 Days
  if (salary_details === 'Monthly'){
    salary_rate = salary_rate / 2
    salRate_allowance = parseFloat(salary_rate) + parseFloat(allowance)
   
  }else{
    salary_rate = salary_rate * 13
    salRate_allowance = parseFloat(salary_rate) + parseFloat(allowance)
    // console.log('This is salAllowance',salRate_allowance)
  }


  if (salRate_allowance <= 15000 && emp_class =='on'){
    CalotherForms = ((90000 - (salary_rate * 2)) / 24)
    CalotherForms = CalotherForms.toFixed(2)
    if(afterDem <= CalotherForms ){
      otherForms = afterDem
      otherForms = otherForms.toFixed(2)
      // document.getElementById('otherForms').value = otherForms;
      // console.log('This is otherForm',otherForms)
    }else{
      otherForms = CalotherForms
      
      // document.getElementById('otherForms').value = otherForms ;
      // console.log('This is otherForm',otherForms)
    }
  }else if  (salRate_allowance <= 15000 && emp_class =='off'){
    // Do nothing, otherForms is already set to 0.00
  }else{
    CalotherForms = (90000-30000) / 24
    CalotherForms = CalotherForms.toFixed(2)
    if(afterDem <= CalotherForms ){
      otherForms = afterDem
      // document.getElementById('otherForms').value = otherForms;
      // console.log('This is otherForm',otherForms)
    }else{
      otherForms = CalotherForms
      
      // document.getElementById('otherForms').value = otherForms ;
      // console.log('This is otherForm',otherForms)
    }

  }
  document.getElementById('otherForms').value = otherForms ;

};

// const calculateOtherForms = async () => {
//   const allowance = parseFloat(document.querySelector('#allowance').value);
//   const totalDeminimis = parseFloat(document.querySelector('#totalDeminimis').value);
//   const salaryDetails = document.querySelector('#salary_details').value;
//   const salaryRate = parseFloat(document.querySelector('#salary_rate').value);
//   const proviRate = parseFloat(document.querySelector('#provi_rate').value);
//   const empClass = document.querySelector('#emp_class').value;

//   const totalGross2 = parseFloat(document.getElementById('totalGross2').value);
//   const basicMWE = proviRate * 13;
//   const basicTaxable = (totalGross2 - basicMWE).toFixed(2);

//   let afterDem = 0.00;

//   if (basicTaxable !== '0.00') {
//     afterDem = (basicTaxable - totalDeminimis);
//   }

//   let salRateAllowance;

//   // Determine if salary is monthly or to get the Total salary for 15 Days
//   let adjustedSalaryRate;

//   if (salaryDetails === 'Monthly') {
//     adjustedSalaryRate = salaryRate / 2;
//     salRateAllowance = adjustedSalaryRate + allowance;
//   } else {
//     adjustedSalaryRate = salaryRate * 13;
//     salRateAllowance = adjustedSalaryRate + allowance;
//   }

//   let otherForms = 0.00;
//   const salAllowanceLimit = 15000;

//   if (salRateAllowance <= salAllowanceLimit && empClass === 'on') {
//     const calOtherForms = ((90000 - (salaryRate * 2)) / 24).toFixed(2);
//     otherForms = (afterDem <= calOtherForms) ? afterDem : calOtherForms;
//     // otherForms = otherForms.toFixed(2);
//   } else if (salRateAllowance <= salAllowanceLimit && empClass === 'off') {
//     // Do nothing, otherForms is already set to 0.00
//   } else {
//     const calOtherForms = ((90000 - 30000) / 24).toFixed(2);
//     otherForms = (afterDem <= calOtherForms) ? afterDem : calOtherForms;
//     // otherForms = otherForms.toFixed(2);
//   }

//   document.getElementById('otherForms').value = otherForms;
// };



const taxComp = async () => {
  

}



    








