$( function() {
                    
    $( "#equipment_id" ).autocomplete({
    source: "/api-search-autocomplete-equipment-rizal/",
    minLength: 1
    });



} );


$(document).ready(function() {
    $('#bucket_Tons, #totalTons_Tons').on('input', function() {
        calculateTotalTons();
    });
    });

    function calculateTotalTons() {

    var Backhoe = $('#Backhoe').val();
    var Bucket = $('#bucket_Tons').val();
    var bachoeValue = 0
    if (Backhoe === 'BH 01' || Backhoe === 'BH 03' ){
        bachoeValue = 2.29
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }else if(Backhoe === 'BH 02'){
        bachoeValue = 1.42
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }
    else if(Backhoe === 'TX 1202' || Backhoe === 'TX 1204'){
        bachoeValue = 1.44
        totalTons = bachoeValue * Bucket
        totalTons2 = parseFloat(totalTons).toFixed(2)
        $('#totalTons_Tons').val(totalTons2);
        calculateProduct_amountTons2()
        calculateProduct_amountTons()
    }

   
    }


$(document).ready(function() {
    $('#totalTons_Tons, #rate_Tons').on('input', function() {
        calculateProduct_amountTons();
    });
    });

    function calculateProduct_amountTons() {

    var totalTons_Tons = $('#totalTons_Tons').val();
    
    var rate_Tons = $('#rate_Tons').val();
    
    var product = totalTons_Tons * rate_Tons;
    
    var product2 = parseFloat(product).toFixed(2)

    $('#amount_Tons').val(product2);
    }



$(document).ready(function() {
    $('#rate_Tons, #totalTons_Tons').on('input', function() {
        calculateProduct_amountTons2();
    });
    });

    function calculateProduct_amountTons2() {

    var totalTons_Tons = $('#totalTons_Tons').val();
    
    var rate_Tons = $('#rate_Tons').val();
    
    var product = totalTons_Tons * rate_Tons;
    
    // var floatValue = product.toLocaleString('en-US');
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#amount_Tons2').val(stringNumber);
    }