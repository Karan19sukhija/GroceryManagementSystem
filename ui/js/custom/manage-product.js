var productModal = $("#productModal");
$(function () {
    //JSON data by API call
    $.get(productListApiUrl, function (response) {
        if(response) {
            var table = '';
            $.each(response, function(index, product) {
                table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                    '<td>'+ product.name +'</td>'+
                    '<td>'+ product.uom_name +'</td>'+
                    '<td>'+ product.price_per_unit +'</td>'+
                    '<td>' +
                    '<span class="btn btn-xs btn-success edit-product" style="margin-right: 5px;">Edit</span>' +
                    '<span class="btn btn-xs btn-danger delete-product">Delete</span>' +
                    '</td></tr>';
            });
            $("table").find('tbody').empty().html(table);
        }
    });
});

// Save Product
$("#saveProduct").on("click", function () {
    // If we found id value in form then update product detail
    var data = $("#productForm").serializeArray();

    var requestPayload = {
        product_id: null,
        product_name: null,
        uom_id: null,
        price_per_unit: null
    };

    var product_id = $('#id').val();
    if (product_id !=0 ){
        requestPayload.product_id = product_id
    }
    console.log("safadf" + requestPayload.product_id);

    for (var i=0;i<data.length;++i) {
        var element = data[i];
        switch(element.name) {
            case 'name':
                requestPayload.product_name = element.value;
                break;
            case 'uoms':
                requestPayload.uom_id = element.value;
                break;
            case 'price':
                requestPayload.price_per_unit = element.value;
                break;
        }
    }
    callApi("POST", productSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});

$(document).on("click", ".delete-product", function (){
    var tr = $(this).closest('tr');
    var data = {
        product_id : tr.data('id')
    };
    var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
    if (isDelete) {
        callApi("POST", productDeleteApiUrl, data);
    }
});


$(document).on("click", ".edit-product", function (){

    // Fetched the values of the product from table row
    var tr = $(this).closest('tr');
    var product_id = tr.data('id');
    var product_name = tr.data('name');
    var price_per_unit = tr.data('price');

    // Set the values in the form input fields in the product Modal
    $('#id').val(product_id);
    $('#name').val(product_name);
    $('#price').val(price_per_unit);
    productModal.find('.modal-title').text('Edit Product');

    // Show the modal in the end
    $('#productModal').modal('show');  // Using Bootstrap's modal method

});


productModal.on('hide.bs.modal', function(){
    $("#id").val('0');
    $("#name, #unit, #price").val('');
    productModal.find('.modal-title').text('Add New Product');
});

productModal.on('show.bs.modal', function(){
    //JSON data by API call
    $.get(uomListApiUrl, function (response) {
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, uom) {
                options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
            });
            $("#uoms").empty().html(options);
        }
    });
});