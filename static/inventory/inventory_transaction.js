const insert_inventory = async () => {
    const data = {
        item_name: document.getElementById("item_name").value,
        description: document.getElementById("description").value,
        category: document.getElementById("category").value,
        uom: document.getElementById("uom").value,
        supplier: document.getElementById("supplier").value,
        price: document.getElementById("price").value,
        quantity_in_stock: document.getElementById("quantity_in_stock").value,
        minimum_stock_level: document.getElementById("minimum_stock_level").value,
        location: document.getElementById("location").value,
        tax_code: document.getElementById("tax_code").value,
    };
     
    console.log(data)
    try {
        const response = await fetch(`/api-insert-inventory-rizal-employee/`, {
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
            window.location.assign("/inventory-frame-rizal/");
        } else {
            window.alert("An unknown error occurred");
        }
    } catch (error) {
        window.alert(error);
        console.log(error);
    }
};

// Attach the event listener to the button
var Btn_Save_inventory = document.querySelector('#Btn_Save_inventory');
Btn_Save_inventory.addEventListener("click", insert_inventory);


const employeeData = async () => {
    try {
      const search_url = '/api-get-inventory-all-rizal-employeeLogin/';
      const response = await fetch(search_url);
      const data = await response.json();
      console.log(data);
  
      const filterData = (searchValue) =>
        data.filter((item) => {
          const item_name = item.item_name.toLowerCase();
          const description = item.description.toLowerCase();
          const category = item.category.toLowerCase();
          const supplier = item.supplier.toLowerCase();
          return (
            item_name.includes(searchValue) ||
            description.includes(searchValue) ||
            category.includes(searchValue) ||
            supplier.includes(searchValue) 
          );
        });
  
      const displayData = (filteredData) => {
        const tbody = document.querySelector('#table_body_inventory');
        tbody.innerHTML = '';
        filteredData.forEach((item, index) => {
          
          const tr = document.createElement('tr');

          // Create a 'td' element for the index
        //   const indexTd = document.createElement('td');
        //   indexTd.textContent = index + 1; // Add 1 to make it start from 1
        //   tr.appendChild(indexTd);

          const item_name = document.createElement('td');
          item_name.textContent = item.item_name;
          const description = document.createElement('td');
          description.textContent = item.description;
          const category = document.createElement('td');
          category.textContent = item.category;
          const uom = document.createElement('td');
          uom.textContent = item.uom;
          const supplier = document.createElement('td');
          supplier.textContent = item.supplier;
          const price = document.createElement('td');
          price.textContent = item.price;
          const quantity_in_stock = document.createElement('td');
          quantity_in_stock.textContent = item.quantity_in_stock;
          const minimum_stock_level = document.createElement('td');
          minimum_stock_level.textContent = item.minimum_stock_level;
          const location = document.createElement('td');
          location.textContent = item.location;
          const tax_code = document.createElement('td');
          tax_code.textContent = item.tax_code;
  
          tr.appendChild(item_name);
          tr.appendChild(description);
          tr.appendChild(category);
          tr.appendChild(uom);
          tr.appendChild(supplier);
          tr.appendChild(price);
          tr.appendChild(quantity_in_stock);
          tr.appendChild(minimum_stock_level);
          tr.appendChild(location);
          tr.appendChild(tax_code);
          tbody.appendChild(tr);
        });
      };
  
      const searchInput = document.querySelector('#inventory_search');
      searchInput.addEventListener('input', (event) => {
        const searchValue = event.target.value.trim().toLowerCase();
        const filteredData = filterData(searchValue);
        displayData(filteredData);
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  employeeData();

// Attach the event listener to the button
// var Btn_Save_inventory = document.querySelector('#Btn_Save_inventory');
// Btn_Save_inventory.addEventListener("click", insert_inventory);

// this function is for autocomple for updating the inventory item
$(document).ready(function() {
  $("#item_name_update").autocomplete({
      source: function(request, response) {
          $.ajax({
              url: "/api-search-autocomplete-inventory-name-rizal/",
              data: { term: request.term },
              dataType: "json",
              success: function(data) {
                  response(data);
              }
          });
      },
      select: function(event, ui) {
          $("#item_id").val(ui.item.id);
          $("#item_name_update").val(ui.item.item_name);
          $("#description_update").val(ui.item.description);
          $("#category_update").val(ui.item.category);
          $("#uom_update").val(ui.item.uom);
          $("#supplier_update").val(ui.item.supplier);
          $("#price_update").val(ui.item.price);
          $("#quantity_in_stock_update").val(ui.item.quantity_in_stock);
          $("#minimum_stock_level_update").val(ui.item.minimum_stock_level);
          $("#location_update").val(ui.item.location);
          $("#tax_code_update").val(ui.item.tax_code);
          
          return false;
      }
  });
});


// this function is for updating the inventory item
const update_inventory_item = async () => {
  const transID = document.getElementById("item_id").value
  const data = {
      item_name: document.getElementById("item_name_update").value,
      description: document.getElementById("description_update").value,
      category: document.getElementById("category_update").value,
      uom: document.getElementById("uom_update").value,
      supplier: document.getElementById("supplier_update").value,
      price: document.getElementById("price_update").value,
      quantity_in_stock: document.getElementById("quantity_in_stock_update").value,
      minimum_stock_level: document.getElementById("minimum_stock_level_update").value,
      location: document.getElementById("location_update").value,
      tax_code: document.getElementById("tax_code_update").value,
  };
   
  console.log(data)
  try {
      if (transID == '') {
        window.alert("No Selected Items");
      }else {
          const response = await fetch(`/api-update-inventory-rizal-employeeLogin/?id=${transID}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const responseData = await response.json();

      
        if (response.status === 401) {
            window.alert("Unauthorized credential. Please login");
        } else if (responseData.error) {
            window.alert("Error: " + responseData.error);
        } else if (response.status === 200) {
            window.alert("Your data has been Updated!!!!");
            window.location.assign("/inventory-frame-rizal/");
        } else {
            window.alert("An unknown error occurred");
        }
      }
      
  } catch (error) {
      window.alert(error);
      console.log(error);
  }
};

// Attach the event listener to the button
var Btn_update_inventory = document.querySelector('#Btn_update_inventory');
Btn_update_inventory.addEventListener("click", update_inventory_item);


// this function is for autocomple of inventory id for  inventory transaction
$(document).ready(function() {
  $("#inventory_transaction_name").autocomplete({
      source: function(request, response) {
          $.ajax({
              url: "/api-search-autocomplete-inventory-name-rizal/",
              data: { term: request.term },
              dataType: "json",
              success: function(data) {
                  response(data);
              }
          });
      },
      select: function(event, ui) {
          $("#inventory_item_id").val(ui.item.id);
          $("#inventory_transaction_name").val(ui.item.item_name);
          $("#unit_price").val(ui.item.price);
          calculateTotalPrice()
          
          
          return false;
      }
  });
});


// this function is for computation of total Price
$(document).ready(function() {
  $('#quantity, #unit_price').on('input', function() {
    calculateTotalPrice();
  });
  });

  function calculateTotalPrice() {

  var quantity = $('#quantity').val();
  
  var unit_price = $('#unit_price').val();
  
  var product = quantity * unit_price;
  
  // var floatValue = product.toLocaleString('en-US');
  const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  $('#total_price').val(stringNumber);
  $('#total_price2').val(product);
  }


//   // this function is for inserting Inventory Transactions

//   const insert_inventory_transaction = async () => {
//     const data = {
//       inventory_item_id: document.getElementById("inventory_item_id").value,
//       transaction_type: document.getElementById("transaction_type").value,
//       transaction_date: document.getElementById("transaction_date").value,
//       quantity: document.getElementById("quantity").value,
//       unit_price: document.getElementById("unit_price").value,
//       total_price: document.getElementById("total_price2").value,
//       mrs_no: document.getElementById("mrs_no").value,
//       si_no_or_withslip_no: document.getElementById("si_no_or_withslip_no").value,
//       end_user: document.getElementById("end_user").value,
        
//     };
     
//     console.log(data)
//     try {
//         const response = await fetch(`/api-insert-inventory-transaction-rizal-employee/`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(data),
//         });

//         const responseData = await response.json();

       
//         if (response.status === 401) {
//             window.alert("Unauthorized credential. Please login");
//         } else if (responseData.error) {
//             window.alert("Error: " + responseData.error);
//         } else if (response.status === 200) {
//             window.alert("Your data has been saved!!!!");
//             window.location.assign("/inventory-frame-rizal/");
//         } else {
//             window.alert("An unknown error occurred");
//         }
//     } catch (error) {
//         window.alert(error);
//         console.log(error);
//     }
// };

// // Attach the event listener to the button
// var Btn_Save_inventory = document.querySelector('#Btn_Save_inventory');
// Btn_Save_inventory.addEventListener("click", insert_inventory_transaction);

// // Function to update inventory item quantity
// function updateInventory() {
//   // Collect data from input fields
//   const inventoryTransactionName = $("#inventory_transaction_name").val();
//   const inventoryItemId = $("#inventory_item_id").val();
//   const transactionType = $("#transaction_type").val();
//   const transactionDate = $("#transaction_date").val();
//   const quantity = $("#quantity").val();
//   const unitPrice = $("#unit_price").val();
//   const totalPrice = $("#total_price").val();
//   const mrsNo = $("#mrs_no").val();
//   const siNoOrWithdrawalSlipNo = $("#si_no_or_withslip_no").val();
//   const endUser = $("#end_user").val();

//   // Create a data object to send in the request
//   const data = {
    
//     quantity: quantity,
//     // Add other fields here as needed
//   };

//   // Send a POST request to your API
//   $.ajax({
//     type: "PUT",
//     url: `/api-update-inventory-item-quantity-rizal-employeeLogin/${inventoryItemId}`,
//     data: JSON.stringify(data),
//     contentType: "application/json",
//     success: function (response) {
//       // Handle success response here, e.g., show a success message
//       // alert("Inventory updated successfully!");
//     },
//     error: function (error) {
//       // Handle error response here, e.g., show an error message
//       console.error("Error updating inventory:", error);
//     },
//   });
// }

// // Attach the updateInventory function to the button click event
// $("#Btn_save_inventory_transactions").on("click", updateInventory);



// Function to update inventory item quantity
const updateInventoryItemQuantity = async () => {
  var itemId = document.getElementById('inventory_item_id').value
  var transactionType = document.getElementById('transaction_type').value
  var quantity = document.getElementById('quantity').value
  const data = {
    transaction_type: transactionType,
    quantity: quantity,
    // Add other fields here as needed
  };

  try {
    const response = await fetch(`/api-update-inventory-item-quantity-rizal-employeeLogin/?id=${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const responseData = await response.json();

    if (response.status === 401) {
      window.alert("Unauthorized credential. Please login");
    } else if (responseData.error) {
      window.alert("Error: " + responseData.error);
    } else if (response.status === 200) {
      // window.alert("Inventory item quantity updated successfully!");
      // You can perform additional actions here after the update is successful
    } else {
      window.alert("An unknown error occurred");
    }
  } catch (error) {
    window.alert(error);
    console.error("Error updating inventory item quantity:", error);
  }
};



// Function to insert Inventory Transactions and trigger updateInventory
const insertInventoryTransactionAndTriggerUpdate = async () => {
  // Insert Inventory Transactions
  const data = {
    inventory_item_id: document.getElementById("inventory_item_id").value,
    transaction_type: document.getElementById("transaction_type").value,
    transaction_date: document.getElementById("transaction_date").value,
    quantity: document.getElementById("quantity").value,
    unit_price: document.getElementById("unit_price").value,
    total_price: document.getElementById("total_price2").value,
    mrs_no: document.getElementById("mrs_no").value,
    si_no_or_withslip_no: document.getElementById("si_no_or_withslip_no").value,
    end_user: document.getElementById("end_user").value,
  };

  try {
    const response = await fetch(`/api-insert-inventory-transaction-rizal-employee/`, {
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
      // Trigger updateInventory after successfully inserting inventory transactions
      updateInventoryItemQuantity()
      window.location.assign("/inventory-frame-rizal/");
    } else {
      window.alert("An unknown error occurred");
    }
  } catch (error) {
    window.alert(error);
    console.log(error);
  }
};

// Attach the event listener to the "Save" button and trigger insertInventoryTransactionAndTriggerUpdate
var BtnSaveInventoryTransactions = document.querySelector('#Btn_save_inventory_transactions');
BtnSaveInventoryTransactions.addEventListener("click", insertInventoryTransactionAndTriggerUpdate);


$(document).ready( function() {
                    
  $( "#end_user" ).autocomplete({
  source: "/api-search-autocomplete-equipment-rizal/",
  minLength: 1
  });
} );

// this function is to display Inventory Transaction List
const  displayInventoryTransactionlist =  async () => {
  var datefrom = document.getElementById("inventory_transaction_list_datefrom").value 
  var dateto = document.getElementById("inventory_transaction_list_dateto").value 
  var category_type = document.getElementById("inventory_transaction_list_category").value 
  var transaction_type = document.getElementById("inventory_transaction_list_transaction_type").value 
  var end_user = document.getElementById("inventory_transaction_list_end_user").value 
  
  const search_url = `/api-get-inventory-transaction-rizal-employeeLogin/?datefrom=${datefrom}&dateto=${dateto}&category_type=${category_type}&transaction_type=${transaction_type}&end_user=${end_user}`;


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
                      <td>${values.transaction_date}</td>
                      <td>${values.item_name}</td>
                      <td>${values.description}</td>
                      <td>${values.quantity}</td>
                      <td>${values.unit_price}</td>
                      <td>${values.total_price}</td>
                      <td>${values.end_user}</td>
                      <td>${values.tax_code}</td>
                      <td>${values.transaction_type}</td>
                     
                  
                  </tr>`;
      });
      document.getElementById("table_body_inventory_transaction_list").innerHTML=tableData;
      // var test = 1000
      // document.getElementById("fter_totalBillinglTons").value = test;
      
  }else if (responce.status === 401){
      window.alert("Unauthorized Credentials Please Log in")
  }

};


var Btn_search_inventory_transactions = document.querySelector('#Btn_search_inventory_transactions');
Btn_search_inventory_transactions.addEventListener("click", displayInventoryTransactionlist);

// Setting the Click Event Listener on the Submit Button
$(document).ready(function(){
  var maxField = 10; //Input fields increment limitation
  var addButton = $('#add_button'); //Add button selector
  var wrapper = $('#addrow'); //Input field wrapper
  var x = 0; //Initial field counter is 1
  
  // });
  //Once add button is clicked
  $(addButton).click(function(){
      //Check maximum number of input fields
      x++; //Increment field counter
      var fieldHTML = `<tr>

      <td>
         
      <div class="col-md">
        <div class="form-floating">
              <input
              type="text" hidden
              name="inventory_item_id${x}"
              id="inventory_item_id${x}"
              class="inventory_item_id"
              style="width: 35px;"
              
              >
              </input
        
        </div>
      </div>
          
          
      </td>

      <td>

      <div class="col-md">
          <div class="form-floating">
              <input
              type="text"
              name="inventory_id_list${x}"
              id="inventory_id_list${x}"
              class="inventory_id_list"
              style="width: 150px;"
              
                >
                </input
            
          </div>
      </div>
        
          
          
      </td>
      

     
      

      <td>
          <div class="col-md">
                <div class="form-floating">
                    <input
                    type="number"
                    name="quantity_list${x}"
                    id="quantity_list${x}"
                    class="quantity_list"
                    step="0.01"
                    
                    style="width: 100px;text-align: right;"
                    
                      >
                      </input
            
                </div>
          </div>


          
      </td>

      <td>
        <div class="col-md">
              <div class="form-floating">
              <input
              type="number"
              name="unit_price_list${x}"
              id="unit_price_list${x}"
              class="unit_price_list"
              step="0.01"
              
              style="width: 100px;text-align: right;"
              
                >
                </input
                
              </div>
        </div>

          
          
      </td>

      <td>

        <div class="col-md">
              <div class="form-floating">
              <input
                  type="number"
                  name="total_price_list${x}"
                  id="total_price_list${x}"
                  class="total_price_list"
                  step="0.01"
                  
                  style="width: 150px;text-align: right;"
                  
              >
              </input
                
              </div>
        </div>
          
      </td>

      <td>

      <div class="col-md">
            <div class="form-floating">
            <input
                type="text"
                name="end_user_list${x}"
                id="end_user_list${x}"
                class="end_user_list"
                step="0.01"
                
                style="width: 150px;text-align: right;"
                
            >
            </input
              
            </div>
      </div>
        
    </td>

    
      <td>
          <button type="button"  id="remove_button" class="btn btn-danger"><i class="fas fa-database">
          </i>X</button>
      </td>
      </tr> `; //New input field html 
      $(wrapper).append(fieldHTML); //Add field html

      // myFunction2();
      
  });




  //Once remove button is clicked
  $(wrapper).on('click', '#remove_button', function(e){
      e.preventDefault();
      $(this).closest('tr').remove(); //Remove field html 
      myFunction2();
      x--; //Decrement field counter
  });

  $(document).on('focus', `[id^="end_user_list"]`, function() {
    $(this).autocomplete({
    source: "/api-search-autocomplete-equipment-rizal/"
    });
    
   
});

// this is for autocomplete for 
$(document).on('focus', `[id^="inventory_id_list"]`, function() {
  $(this).autocomplete({
    source: function(request, response) {
      $.ajax({
        url: "/api-search-autocomplete-inventory-name-rizal/",
        data: { term: request.term },
        dataType: "json",
        success: function(data) {
          response(data);
          
        }
      });
    },
    minLength: 1, // Minimum number of characters to trigger autocomplete
    select: function(event, ui) {
      // Get the current x value from the ID of the input field
      var x = this.id.match(/\d+/)[0];

      $("#inventory_id_list" + x).val(ui.item.item_name);
      $("#unit_price_list" + x).val(ui.item.price);
      $("#inventory_item_id" + x).val(ui.item.id);

      var unitPrice = parseFloat($("#unit_price_list" + x).val());
      var quantity = parseFloat($("#quantity_list" + x).val());
      var totalPrice = unitPrice * quantity;

      $("#total_price_list" + x).val(totalPrice.toFixed(2)); // Set the value with 2 decimal places
      
      myFunction2()
      return false;
    }
  });
});


});


// this function is for total Amount
function myFunction2() {
  let totalPriceElements = document.getElementsByClassName('total_price_list');
  let total_price_sum = 0;

  for (let i = 0; i < totalPriceElements.length; i++) {
    let totalValue = parseFloat(totalPriceElements[i].value);
    if (!isNaN(totalValue)) {
      total_price_sum += totalValue;
    }
  }

  total_price_sum = total_price_sum.toFixed(2);
  document.getElementById('TotalAmount').value = total_price_sum;
}





// this function is for inserting data to inventory transactions

const insert_inventory_transaction_list = async () => {
  // Create an array to store the data for each row
 
  const rowData = [];
  const elements = document.querySelectorAll('[id^="inventory_id_list"]');
  elements.forEach((element) => {
    const inputValue = element.value;
    const inventoryItemID = document.querySelector(`#${element.id.replace('inventory_id_list', 'inventory_item_id')}`).value;
    const quantity = document.querySelector(`#${element.id.replace('inventory_id_list', 'quantity_list')}`).value;
    const unitPrice = document.querySelector(`#${element.id.replace('inventory_id_list', 'unit_price_list')}`).value;
    const totalPrice = document.querySelector(`#${element.id.replace('inventory_id_list', 'total_price_list')}`).value;
    const endUser = document.querySelector(`#${element.id.replace('inventory_id_list', 'end_user_list')}`).value;

    const trans_type = document.querySelector(`#transaction_type_list`).value;
    const trans_date = document.querySelector(`#transaction_date_list`).value;
    const mrs = document.querySelector(`#mrs_no_list`).value;
    const si_withdrawal_no = document.querySelector(`#si_no_or_withslip_no_list`).value;

    // Create an object for each row of data
    const rowDataItem ={
      inventory_item_id: inventoryItemID,
      transaction_type: trans_type,
      transaction_date: trans_date,
      quantity: quantity,
      unit_price: unitPrice,
      total_price: totalPrice,
      mrs_no: mrs,
      si_no_or_withslip_no: si_withdrawal_no,
      end_user: endUser,
    };
   
   // Add the row's data object to the rowData array
   rowData.push(rowDataItem);
    
  
  });

  // Iterate over rowData (array of objects)
  rowData.forEach(async (item) => {
    console.log(item);
  
    // Perform custom processing for each item here
   

    try {
      const response = await fetch('/api-insert-inventory-transaction-rizal-employee-testing/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(item), // Send the current item as JSON
      });

      const responseData = await response.json();
  
      if (response.status === 401) {
        window.alert("Unauthorized credential. Please login");
      } else if (responseData.error) {
        window.alert("Error: " + responseData.error);
  
      } else if (response.status === 200) {

        await updateInventoryItemQuantity2(
          item.inventory_item_id,
          item.transaction_type,
          item.quantity
        );

        window.alert("Your data has been saved!!!!");
        // Trigger updateInventory after successfully inserting inventory transactions
      
       
        window.location.assign("/inventory-frame-rizal/");
      } else {
        window.alert("An unknown error occurred");
      }
    } catch (error) {
      window.alert(error);
      console.log(error);
    }
  });
  

  
  
  
};

var Btn_save_inventory_list = document.querySelector('#Btn_save_inventory_list');
Btn_save_inventory_list.addEventListener('click', insert_inventory_transaction_list);


const updateInventoryItemQuantity2 = async (itemId, transactionType, quantity) => {
  const data = {
    transaction_type: transactionType,
    quantity: quantity,
    // Add other fields here as needed
  };

  try {
    const response = await fetch(`/api-update-inventory-item-quantity-rizal-employeeLogin/?id=${itemId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const responseData = await response.json();

    if (response.status === 401) {
      window.alert("Unauthorized credential. Please login");
    } else if (responseData.error) {
      window.alert("Error: " + responseData.error);
    } else if (response.status === 200) {
      // window.alert("Inventory item quantity updated successfully!");
      // You can perform additional actions here after the update is successful
    } else {
      window.alert("An unknown error occurred");
    }
  } catch (error) {
    window.alert(error);
    console.error("Error updating inventory item quantity:", error);
  }
};



function html_table_excel(type) {
  var data = document.getElementById('table_body_inventory_transaction_list');
  var file = XLSX.utils.table_to_book(data, { sheet: "sheet1" });
  XLSX.write(file, { booktype: type, bookSST: true, type: 'base64' });
  XLSX.writeFile(file, 'inventory.' + type);
}


