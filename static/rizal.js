
const printRentalPDF = async () => {

    var datefrom = document.getElementById("datefrom").value;
    var dateto = document.getElementById("dateto").value;
    var equipmentID = document.getElementById("equipment_id_searchRental").value;
  
    const search_url = `/api-get-rental-rizal-employee_login/?datefrom=${datefrom}&dateto=${dateto}&equipment_id=${equipmentID}`;
  
    const response = await fetch(search_url);
    const dataSet = await response.json();
    
      const docDefinition = {
        pageOrientation: 'landscape',
        content: [
          { text: 'LD GLOBAL LEGACY', style: 'header' },
          { text: 'EQUIPMENT RENTAL REPORT', style: 'header' },
          { text: `COVERAGE : Date From: ${datefrom}  AND  Date TO: ${dateto}`, style: 'header' },
          { text: '\n' },
          {
            table: {
              headerRows: 1,
              widths: ['auto', 'auto', 'auto', 'auto'],
              body: [
                ['Equipment ID', 'Total Hours', 'Total Amount', 'Entries'],
                ...generateTableRows(dataSet),
              ],
            },
            layout: {
              defaultBorder: false,
              paddingTop: function (i, node) { return 5; },
              paddingBottom: function (i, node) { return 5; },
            },
          },
        ],
        styles: {
          header: {
            fontSize: 15,
            bold: true,
            alignment: 'center',
          },
          bodyText: {
            fontSize: 10,
            alignment: 'right',
          },
          entryText: {
            fontSize: 9,
            bold: false,
            alignment: 'right',
          },
        },
      };
      
      function generateTableRows(dataSet) {
        const rows = [];
        const groupedData = groupDataByEquipment(dataSet);
      
        Object.entries(groupedData).forEach(([equipmentId, equipmentData]) => {
          rows.push([
            equipmentId,
            equipmentData.total_rental_hour ? equipmentData.total_rental_hour.toLocaleString("en-US") : '',
            equipmentData.rental_amount ? equipmentData.rental_amount.toLocaleString("en-US") : '',
            generateEntriesTable(equipmentData.entries),
          ]);
        });
      
        return rows;
      }
      
      function groupDataByEquipment(dataSet) {
        const groupedData = {};
        dataSet.forEach((data) => {
          const { equipment_id, total_rental_hour, rental_amount } = data;
          if (!groupedData[equipment_id]) {
            groupedData[equipment_id] = {
            total_rental_hour: 0,
            rental_amount: 0,
              entries: [],
            };
          }
          groupedData[equipment_id].total_rental_hour += parseFloat(total_rental_hour);
          groupedData[equipment_id].rental_amount += parseFloat(rental_amount);
          groupedData[equipment_id].entries.push(data);
        });
        return groupedData;
      }
      
      function generateEntriesTable(entries) {
        const body = [
          [
            { text: 'ID', style: 'entryText' },
            { text: 'Trans Date', style: 'entryText' },
            { text: 'EUR', style: 'entryText' },
            { text: 'Total Hours', style: 'entryText' },
            { text: 'Rental Rate', style: 'entryText' },
            { text: 'Rental Amount', style: 'entryText' },
          ],
          ...entries.map((entry) =>  [
           
            { text: entry.id.toString(), style: 'entryText' },
            { text: entry.transaction_date, style: 'entryText' },
            { text: entry.eur_form, style: 'entryText' },
            { text: entry.total_rental_hour, style: 'entryText' },
            { text: entry.rental_rate, style: 'entryText' },
            { text: entry.rental_amount, style: 'entryText' },
            // entry.transaction_date,
            // entry.eur_form,
            // entry.total_rental_hour.toLocaleString("en-US"),
            // entry.rental_amount.toLocaleString("en-US"),
          ]),

        

          

        ];
      
        return {
          table: {
            widths: ['auto', 'auto', 'auto', 'auto', 'auto', 'auto'],
            body,
          },
          layout: 'lightHorizontalLines',
        };
      }

      
      
      const pdfDoc = pdfMake.createPdf(docDefinition);
      pdfDoc.download('equipment_hauling_report.pdf');
      
}

const BTN_printRentalPDF = document.querySelector('#printRentalPDF');
BTN_printRentalPDF.addEventListener("click", printRentalPDF);  