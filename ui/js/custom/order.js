var productPrices = {};

$(function () {
    //Json data by api call for order table
    $.get(productListApiUrl, function (response) {
        productPrices = {}
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    // We will add the new product item row only if the previuos product item row has a select value from dropdown

    // Check if a child div with the class 'product-box' exists
    const $productBoxExtra = $('.product-box-extra');

    // Check if a child div with the class 'product-item' exists.
    if ($productBoxExtra.find('.product-item').length == 0) {
        // It means it is the 1st time the row is getting added
        addProductRow();
    }
    else{
        const $lastProductBox = $(".product-box-extra .product-item").last();
        const $lastDropdown = $lastProductBox.find('.cart-product').last();
        // Check if a value is selected in the last dropdown
        if ($lastDropdown.val()){
            addProductRow(); 
        } else {
            alert('Please select the product in the current dropdown before adding a new one.');
        }
    }

});

function addProductRow() {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().text('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().text('0.0');
}

$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

// Enabling the save button only when customer named ( except spaces ) is entered.
$("#customerName").on('input', function(){
    if ($('#customerName').val().trim() !== ''){
        $("#saveOrder").prop('disabled', false);
    } else {
        $("#saveOrder").prop('disabled', true);
    }
});

$("#saveOrder").on("click", function(){
    // serialize Array will give the array of maps. Each map represents an element of form where key is the name and value 
    // is the input or selected value of that element

    // Removing the last div tag of the product item before serializing the array IF there is no selection of the product 
    // from the dropdown

    const lastProductItem = $('form .product-item').last();
    const $select = lastProductItem.find('select');

    // If the select element has no selected option (empty value)
    if ($select.length > 0 && !$select.val()) {
        // Remove that select element div completely from the form
        lastProductItem.remove();
    }


    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: null,
        grand_total: null,
        order_details: []
    };

    for(var i=0;i<formData.length;++i) {
        var element = formData[i];
        var lastElement = null;

        switch(element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value;
                break;
            case 'product_grand_total':
                requestPayload.grand_total = element.value;
                break;
            case 'product':
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.quantity = element.value
                break;
            case 'item_total':
                if (element.value == 0.00 || element.value == ""){
                    // ignore the row item
                    break;
                }
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.total_price = element.value
                break;
        }

    }
    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});

