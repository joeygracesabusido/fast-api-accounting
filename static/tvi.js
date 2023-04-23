
                
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
