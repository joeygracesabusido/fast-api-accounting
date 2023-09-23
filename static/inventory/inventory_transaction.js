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
          $("#tax_code").val(ui.item.tax_code);
          
          return false;
      }
  });
});
  