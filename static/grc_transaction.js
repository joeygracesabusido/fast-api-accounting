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
       
    });
    });

    // $(document).ready(function() {
    //     $('#total_rental_hour2,#rentalRateInsertRental').change(function (){
    //         const value1 = $('#total_rental_hour2').val() ;
    //         const value2 = $('#rentalRateInsertRental').val() ;
        
    //         const product = parseFloat(value1) * parseFloat(value2);
    //         console.log(product)
    //         var formattedAmount = product.toLocaleString("en-US", { style: "currency", currency: "USD" });
        
    //         $('#total_amount').val(product);

    //     });
        
    // });

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
