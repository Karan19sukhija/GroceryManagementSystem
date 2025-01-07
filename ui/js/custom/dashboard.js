$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);
                table += '<tr data-id="'+ order.order_id +'">' +
                    '<td>'+ order.datetime +'</td>'+
                    '<td>'+ order.order_id +'</td>'+
                    '<td>'+ order.customer_name +'</td>'+
                    '<td>'+ Number(order.total).toFixed(2) +'$</td>' + 
                    '<td>' + '<a href="order_detail.html?order_id='+ order.order_id + '"><span class="btn btn-xs btn-success view-order" style="margin-right: 5px;">View</span></a>' +
                    '<span class="btn btn-xs btn-danger delete-order">Delete</span>' + '</td>/tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ Number(totalCost).toFixed(2) +'$</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});

$(document).on("click", ".delete-order", function (){
    var tr = $(this).closest('tr');
    var data = {
        order_id : tr.data('id')
    };
    var isDelete = confirm("Are you sure to delete this order?");
    if (isDelete) {
        callApi("POST", orderDeleteApiUrl, data);
    }
});
