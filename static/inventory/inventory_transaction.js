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
