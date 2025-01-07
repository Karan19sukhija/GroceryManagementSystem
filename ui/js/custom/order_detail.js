$(function (){
    // Get the query string from the URL
    var urlParams = new URLSearchParams(window.location.search);
    // Get the order_id from the URL
    var order_id = urlParams.get('order_id');

    $.post(orderDetailsListApiUrl, { order_id: order_id }, function (response) {
        if(response) {

            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total_price);
                table += '<tr data-id="'+ order_id +'">' +
                    '<td>'+ order.name +'</td>'+
                    '<td>'+ order.quantity +'</td>'+
                    '<td>'+ Number(order.total_price).toFixed(2) +'$</td>'+
                    '<td>'+ order.price_per_unit +'</td></tr>';
            });
            table += '<tr><td colspan="2" style="text-align: end"><b>Total</b></td><td><b>'+ Number(totalCost).toFixed(2) +'$</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });

});