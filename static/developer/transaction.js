 // this function is for displaying Admin  Transaction 
 const  displayAdminLogin =  async () => {
   
    
    const search_url = `/api-developer-admin-credentials`;


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
                        <td>${values.fullname}</td>
                        <td>${values.username}</td>
                        <td>${values.status}</td>
                        
                    
                    </tr>`;
        });
        document.getElementById("table_body_admin").innerHTML=tableData;
        
    }else if (responce.status === 401){
        window.alert("Unauthorized Credentials Please Log in")
    }

};


var Btn_admin_login_display = document.querySelector('#admin-login-button');
Btn_admin_login_display.addEventListener("click", displayAdminLogin);


// this function is for displaying Employee  Transaction 
const  displayEmployeeLogin =  async () => {
   
    
    const search_url = `/api-developer-employee-credentials`;


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
                        <td>${values.fullname}</td>
                        <td>${values.username}</td>
                        <td>${values.status}</td>
                        
                    
                    </tr>`;
        });
        document.getElementById("table_body_employee").innerHTML=tableData;
        
    }else if (responce.status === 401){
        window.alert("Unauthorized Credentials Please Log in")
    }

};


var Btn_employee_login_display = document.querySelector('#employee-login-button');
Btn_employee_login_display.addEventListener("click", displayEmployeeLogin);



// Define the InsertTons function
const  InsertAccessSetting = async () => {
    // Get the values of the input fields
    const data = {
        user_id: document.getElementById("user_id").value,
        username: document.getElementById("user_name").value,
        accounting_write: document.getElementById("accounting_write").value,
        accounting_read: document.getElementById("accounting_read").value,
        payroll_write: document.getElementById("payroll_write").value,
        payroll_read: document.getElementById("payroll_read").value,
        site_transaction_write: document.getElementById("site_transaction_write").value,
        site_transaction_read: document.getElementById("site_transaction_read").value,
        inventory_write: document.getElementById("inventory_write").value,
        inventory_read: document.getElementById('inventory_read').value,
       
       
        
         
    };
   
    console.log(data)

    if (data.user_id == '' || data.username == '') {
        window.alert("Please fill up userID and username");
    } else {
        try {
            const response = await fetch(`/api-insert-login-credential-developer`,{
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            // Check if the response was successful
            if (response.status === 200) {
                window.alert("Your data has been saved");
                console.log(data);
                window.location.assign("/developer-transaction/");
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
var Btn_save_access = document.querySelector('#Btn_Save_Access');
Btn_save_access.addEventListener("click", InsertAccessSetting);


