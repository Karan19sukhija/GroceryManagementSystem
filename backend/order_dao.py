from datetime import datetime

from sql_connection import get_sql_connection


def get_order_details(connection, order_id ):

    cursor = connection.cursor()
    try:
        query = ("SELECT order_details.order_id,order_details.product_id, order_details.quantity, order_details.total_price,products.name, products.price_per_unit FROM grocery_store.order_details left join grocery_store.products on order_details.product_id = products.product_id where order_details.order_id = %s")
        data = (order_id,)
        cursor.execute(query, data)

        rows = cursor.fetchall()

        response = []
        for (order_id, product_id, quantity, total_price, name, price_per_unit) in rows:
            response.append({
                "name": name,
                "quantity": quantity,
                "total_price": total_price,
                "price_per_unit": price_per_unit
            })
        return response
    except Exception as err:
        print(f'The error while performing sql query for getting order details: {err}')
    finally:
        cursor.close()


def get_all_orders(connection):
    cursor = connection.cursor(buffered=True)
    try:
        response = []
        query = ("SELECT * FROM grocery_store.orders")
        cursor.execute(query)
        connection.commit()

        # Before executing a new query with the same cursor, make sure all results from any prior query are fetched.
        # If you don’t fetch the results, the cursor still holds the unread results, leading to the "Unread
        # result found" error.
        # Fetch all rows from the previous query

        rows = cursor.fetchall()
        # Now get order_details for each order
        for (order_id, customer_name, total, dt) in rows:
            response.append({
                "order_id": order_id,
                "customer_name": customer_name,
                "total": total,
                "datetime": dt
                # "order_details": get_order_details(order_id, connection)
            })
        return response
    except Exception as err:
        print(f'The error while performing sql query for get all orders: {err}')
    finally:
        cursor.close()


def insert_new_order(connection, order):
    cursor = connection.cursor()
    try:
        # Update if `id` is not None
        if order.get("order_id"):
            print(order)
            # This is a parameterized query as we have to pass data into it
            query = ("UPDATE orders SET customer_name = %(customer_name)s, total = %(total)s, datetime = %(datetime)s WHERE order_id = %(order_id)s;")
            data = {
                "customer_name": order["customer_name"],
                "total": order["grand_total"],
                "datetime": datetime.now(),
                "order_id": order["order_id"]
            }
            # Make sure data is committed to the database
            cursor.execute(query, data)
            order_id = cursor.lastrowid
        else:
            # Insert if `id` is Null
            # Query for Order
            print(f'Order details: {order}')
            order_query = ("INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")
            data = (order["customer_name"], order["grand_total"], datetime.now())

            cursor.execute(order_query, data)
            order_id = cursor.lastrowid
            # Make sure data is committed to the database
            connection.commit()

            order_details_query = (
                "INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")

            order_details_data = []
            for order_detail_record in order["order_details"]:
                data = [order_id, int(order_detail_record["product_id"]), float(order_detail_record["quantity"]), float(order_detail_record["total_price"])]
                order_details_data.append(data)

            cursor.executemany(order_details_query, order_details_data)
            order_id = cursor.lastrowid

            # Make sure data is committed to the database
            connection.commit()

        return order_id
    except Exception as err:
        print(f'The error while performing sql query for insert/update of order: {err}')
    finally:
        cursor.close()


def delete_order(connection, order_id):
    cursor = connection.cursor()
    try:
        query = ("DELETE FROM orders where order_id=" + str(order_id))
        cursor.execute(query)

        # Make sure data is committed to the database
        connection.commit()
    except Exception as err:
        print(f'The error while performing sql query for deletion of order: {err}')
    finally:
        cursor.close()


# making the code modular
if __name__ == "__main__":
    connection = get_sql_connection()
    if connection is not None:
        # print(get_all_orders(connection))
        print(get_order_details(7, connection))
        #print(delete_order(connection, 2))

"""        print(insert_new_order(connection, {
            'customer_name': 'Hulk',
            'grand_total': '100',
            'datetime': datetime.now(),
            'order_id': None,
            'order_details': [{
                'product_id': 7,
                'total_price': 20,
                'quantity': 2
            }, {
                'product_id': 10,
                'total_price': 6,
                'quantity': 2
            }]
        }))"""