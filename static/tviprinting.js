//=================================This is for Printing TVI Voucher=================================
var underlineButton = document.querySelector('#print_jv_modal');
underlineButton.addEventListener("click", function(event) {
event.preventDefault();
// Add your button functionality here
});

const JVData = {


    company: 'LD GLOBAL LEGACY INC.',
    address: '0090 OAKLAND ST. GLORIA VISTA SUBD. SAN RAFAEL, RODRIGUEZ (MONTALBAN), RIZAL',
    tin: 'TIN: 007-241-244',
    
    
    

};


const generateInvoicePDF = async(JVData) => {
    const ref = document.querySelector("#referenceNum").value
    

    const search_url = `/api-tvi-report-printing-jv/?ref=${ref}`;


    const responce = await fetch(search_url)
    const items = await responce.json();
    console.log(items)

    let sumDedit = items.reduce((total, item) => total + item.debit_amount, 0);
    let sumCredit = items.reduce((total, item) => total + item.credit_amount, 0);
    sumDedit = sumDedit.toLocaleString("en-US");
    sumCredit = sumCredit.toLocaleString("en-US");

    let user = items[0].user;

    let totalDebit = 0;
    let totalCredit = 0;
    
    const { company, address, tin,} = JVData;

    // Create a document definition using pdfmake syntax

    const pageSize = {
    width: 8.5 * 72,  // Convert inches to points (1 inch = 72 points)
    height: 13 * 72
    };
    const docDefinition = {
    pageOrientation: 'portrait',
    pageSize: pageSize,
    content: [
        { text: `${company}`, style: 'header' },
        { text: `${address}`, style: 'header2' },
        { text: `${tin}`, style: 'header2' },
        { text: `TVI ZAMBOANGA PROJECT`, style: 'header2' },
        ' ',
        
        
        ' ',
        { text: 'JOURNAL VOUCHER', style: 'header' },
        {
        table: {
            headerRows: 1,
            body: [
            ['Date', 'Particular', 'Reference', 'Acct Num','Discription','Debit','Credit'],
            ...items.map((item) =>
                {
                    const debit = item.debit_amount || 0;;
                    const credit = item.credit_amount || 0;;
                    totalDebit += debit;
                    totalCredit += credit;
                    
                    return [
                        new Date(item.date_entry).toLocaleDateString('en-US'),
                        item.descriptions,
                        item.ref,
                        item.acoount_number,
                        item.account_disc,
                        debit.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
                        credit.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
                    ];
                }),
                    ['Total', '', '', '', '', totalDebit.toLocaleString('en-US',
                     { minimumFractionDigits: 2, maximumFractionDigits: 2}), 
                     totalCredit.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })],
                ]

        },
        layout: 'lightHorizontalLines',
        style: 'bodyText'
        },
        ' ',
        
        // {
        //     columns: [
                
        //         {
        //             text: `Total  Debit   ${sumDedit}`,
        //             style: 'summaryStyle'
        //         },
        //         {
        //             text:  `Total Credit   ${sumCredit}`,
        //             style: 'totalAmount'
        //         }
        //     ],
        //     columnGap: 5, // Spacing between the two columns
        //     // margin: [0, 10, 0, 5], // Margins for the entire element
        // },
        ' ',
        {
        columns:[
            { text: 'Prepared by:', style: 'preparedBY' },
            { text: 'Checked by:', style: 'checkedBY' },
            { text: 'Checked by:', style: 'checkedBY' },
        ],
        columnGap: 5,
        },

        ' ',
        ' ',

        {
            columns:[
                // { text: `${user}`, style: 'perPrepared' },
                { text: `${user}`, style: 'perPrepared' },
                { text: `Roy Saltarin`, style: 'perPrepared' },
                { text: `Jerome Sabusido`, style: 'perPrepared' }
            ],
            columnGap: 1,
        },

        {
            columns:[
                
                { text: 'Accounting Asst', style: 'perPrepared' },
                { text: 'Accounting Asst', style: 'perPrepared' },
                { text: 'Accounting Asst', style: 'perPrepared' },
            ],
            columnGap: 5,
        }
        
    
        

    ],
    styles: {
        bodyText: {
            fontSize: 10,
            fonts: 'Courier'
            
        }, 
        header: {
        fontSize: 15,
        bold: true,
        alignment: 'center',
        margin: [25, 0, 0, 10]
        },
        header2: {
            fontSize: 10,
            bold: false,
            alignment: 'center',
            margin: [25, 0, 0, 10]
        },
        subheader: {
        fontSize: 14,
        bold: true,
        margin: [0, 10, 0, 5]
        },

        preparedBY:{
            fontSize: 10,
            bold: false,
            margin: [10, 10, 20, 5],
        },

        checkedBY:{
            fontSize: 10,
            bold: false,
            margin: [17, 10, 20, 1],
            },

        

        perPrepared:{
            fontSize: 10,
            bold: false,
            margin: [20, 10, 20, 1],

    


        checkedBYperson:{
            fontSize: 8,
            bold: false,
            margin: [10, 10, 20, 5],
            },
        },
        summaryStyle: {
            fontSize: 10,
            bold: false,
            alignment: 'right', // Align the element to the right
            margin: [0, 10, 20, 0], // Adjust other margin values as needed
        },
        totalAmount: {
            fontSize: 10,
            bold: false,
            alignment: 'left', // Align the element to the left
            margin: [0, 10, 20, 0], // Adjust other margin values as needed
        },

        totalStyle: {
            fontSize: 10,
            alignment: 'right'
            },
        doubleUnderline: {
            decoration: 'underline',
            decorationStyle: 'double'
            },

    },
    
    };

    

    // Generate the PDF
    const pdfDocGenerator = pdfMake.createPdf(docDefinition);
    pdfDocGenerator.download('jourvalVoucher.pdf');
}

var BtnPdf_Tons = document.querySelector('#Btn_print_JV');
BtnPdf_Tons.addEventListener("click", function() {
generateInvoicePDF(JVData);
});
