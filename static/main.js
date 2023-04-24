// ============================This is for function of Displaying Query for Employee================
$(document).ready(function() {
  $('#myCheckbox2').change(function() {
  if($(this).prop('checked')) {
  
      // deminimis_computation()
      // deminimis_computation1()
      console.log('I am Legend')
  

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
        deminimis_computation()
 
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
    

    salary_details = document.getElementById('salary_details').value;
    salary_rate = document.getElementById('salary_rate').value

    if (salary_details == 'Monthly'){
        salary_rate = salary_rate
    }else{
        salary_rate = salary_rate * 26
    }
    
    const search_url = `/sss-computation/`;

    const responce = await fetch(search_url)
    const data = await responce.json();

    for (let i of data){
        if (i.amountTo >= salary_rate && i.amountFrom <= salary_rate){
            sssAmount = i.empShare
            sssAmount = sssAmount.toFixed(2)
            document.getElementById('sss').value = sssAmount
            calculateTotalGov()
        }

    }

    if (salary_rate <= 10000){
        phic = 400 /2
        phic = phic.toFixed(2)
        document.getElementById('phic').value = phic
        calculateTotalGov()

    }else if(salary_rate > 10000){
        phic = salary_rate * 0.04 / 2
        phic = phic.toFixed(2)
        document.getElementById('phic').value = phic
        calculateTotalGov()
    }else if(salary_rate >= 80000){
        phic = 3200
        phic = phic.toFixed(2)
        document.getElementById('phic').value = phic
        calculateTotalGov()

    }
    hdmf = 100
    document.getElementById('hdmf').value = hdmf
    calculateTotalGov()


    sssProv = document.getElementById('sssProv').value;

    if (sssProv == ''){
        sssProv = 0.00
        document.getElementById('sssProv').value = sssProv;
        calculateTotalGov()


    }
    
    // console.log(data.length)
      
};

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





