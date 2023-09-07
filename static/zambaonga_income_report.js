const printIncomeReport = async () => {
    const datefrom = document.querySelector("#trans_date_from").value;
    const dateto = document.querySelector("#trans_date_to").value;

    const search_url = `/api-income-statement-zamboanga/?datefrom=${datefrom}&dateto=${dateto}`;

    const response = await fetch(search_url);
    const data = await response.json();

    // Create an object to group data by bsClass
    const groupedData = {};

    // Iterate through the data and group by bsClass
    data.forEach(item => {
        const { bsClass } = item;

        if (!groupedData[bsClass]) {
            // If the bsClass key doesn't exist in the groupedData object, create an empty array
            groupedData[bsClass] = [];
        }

        // Push the item to the corresponding bsClass array
        groupedData[bsClass].push(item);
    });

    // Calculate and add Gross Income, Cost of Sales, and General & Administrative totals
    let grossIncome = 0;
    let costOfSales = 0;
    let generalAndAdmin = 0;

    // Create an array to store the tables and totals for each bsClass
    const tables = [];

    // Define the desired order of categories
    const desiredOrder = ['Income', 'Cost of Sales', 'General & Administrative'];

    // Define the desired order of categories
    const categoryOrder = ['Income', 'Cost of Sales', 'General & Administrative'];

    // Iterate through categories in the desired order
    categoryOrder.forEach(category => {
        const categoryData = groupedData[category];

        if (categoryData) {
            categoryData.forEach(item => {
                if (category === 'Income') {
                    grossIncome += item.amount;
                } else if (category === 'Cost of Sales') {
                    costOfSales += item.amount;
                } else if (category === 'General & Administrative') {
                    generalAndAdmin += item.amount;
                }
            });
        }
    });

    // Iterate through desired categories and create tables and totals
    desiredOrder.forEach(categoryName => {
        const categoryData = groupedData[categoryName];

        

        if (categoryData) {
            const table = {
                style: 'table',
                table: {
                    widths: ['auto', '*', 'auto', '*'],
                    body: [],
                    // Set the border color to white
                    borderColor: '#FFFFFF',
                    // Set a smaller line width to make the borders appear thinner
                    lineWidth: 0.05,
                },
            };

            table.table.body.push(['Account Number', 'Account Name', 'Amount', 'Total Amount']); // Table header

            let totalAmount = 0; // Initialize the total amount

            categoryData.forEach(item => {
                table.table.body.push([item.account_number, item.accountName, numberWithCommas(item.amount.toFixed(2)), '']); // Add an empty column for the total
                totalAmount += item.amount; // Add the amount to the total
            });

            tables.push({ text: categoryName, style: 'header' });
            tables.push(table);

            // Add the total amount in line with the amounts
            tables[tables.length - 1].table.body.push(['Total', '', '', numberWithCommas(totalAmount.toFixed(2))]);
        }
    });

    // Calculate net income
    const netIncome = grossIncome - costOfSales - generalAndAdmin;

    // Add a section for Net Income
    const netIncomeSection = {
        text: 'Net Income',
        style: 'header', // You can define a 'header' style in your styles definition
    };

    const netIncomeTable = {
        style: 'table',
        table: {
            widths: ['auto', '*', 'auto'],
            body: [
                ['Net Income', '', numberWithCommas(netIncome.toFixed(2))],
            ],
        },
    };

    tables.push(netIncomeSection);
    tables.push(netIncomeTable);

    // Create and open the PDF
    const docDefinition = {
        content: tables,
        defaultStyle: {fontSize: 10},
    };

    pdfMake.createPdf(docDefinition).open();
};

const BtnPdf_print = document.querySelector('#Btn_print');
BtnPdf_print.addEventListener("click", function () {
    printIncomeReport();
});

// Function to add thousand separators
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
