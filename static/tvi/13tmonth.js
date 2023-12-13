// this function is for displaying 13th month Transaction 
const  display_13month =  async () => {
    var datefrom = document.getElementById("datefrom_13month").value || ''
    var dateto = document.getElementById("dateto_13thmonth").value || ''
    var employeeID = document.getElementById("employeeID_13month_search").value || ''
    
    const search_url = `/tvi-13month-list/?datefrom=${datefrom}&dateto=${dateto}&employeeID=${employeeID}`;


    const responce = await fetch(search_url)
    const data = await responce.json();
    console.log(data)

    if (data.length === 0) {
            window.alert('No Data available');
        };
    
    
    if (responce.status === 200){
        let tableData="";
        let sum = 0;
        data.payrollData.map((values, index)=>{
            const columnNumber = index + 1; 
            
            tableData+= ` <tr>
                        <td>${columnNumber}</td>
                        <td>${values.employee_id}</td>
                        <td>${values.last_name}</td>
                        <td>${values.first_name}</td>
                        <td>${values.salaryRate}</td>
                        <td>${values.regDay}</td>
                        <td>${values.sunday}</td>
                        <td>${values.spl}</td>
                        <td>${values.lgl2}</td>
                        <td>${values.lgl1}</td>
                        <td>${values.total_no_days}</td>
                        <td>${values.total_amount_13_2}</td>
                    </tr>`;
        });
        document.getElementById("table_body_13thmonth").innerHTML=tableData;
        document.getElementById('total_amount_13thmonth').value = data.totalAmount
        // var test = 1000
        // document.getElementById("fter_totalBillinglTons").value = test;
        sumtoTalAmountDiesel()
    }else if (responce.status === 401){
        window.alert("Unauthorized Credentials Please Log in")
    }

};


var BtnSearch_13month = document.querySelector('#BtnSearch_13thmonth');
BtnSearch_13month.addEventListener("click", display_13month);
