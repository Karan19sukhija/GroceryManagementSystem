# DAO - Data access object
# You need a library called mysql-connector-python. Install it by running:
# pip3 install mysql-connector-python


from sql_connection import get_sql_connection


def get_all_products(connection):
    cursor = connection.cursor()
    response = []
    try:
        query = ("SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name"
                 " FROM grocery_store.products inner join grocery_store.uom on products.uom_id = uom.uom_id")
        cursor.execute(query)

        for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
            response.append({
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name
            })

        return response
    except Exception as err:
        print(f'The error while performing sql query for getting all products: {err}')
    finally:
        cursor.close()


def insert_new_product(connection, product):
    cursor = connection.cursor()
    try:
        # Update if `id` is not Null
        if product["product_id"]:
            print(product)
            # This is a parameterized query as we have to pass data into it
            query = ("UPDATE products SET name = %(product_name)s, uom_id = %(uom_id)s, price_per_unit = %(price_per_unit)s WHERE product_id = %(product_id)s;")
            data = {
                "product_name": product["product_name"],
                "uom_id": product["uom_id"],
                "price_per_unit": product["price_per_unit"],
                "product_id": product["product_id"]
            }
        else:
            # Insert if `id` is Null
            query = ("INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)")
            data = (product["product_name"], product["uom_id"],product["price_per_unit"])

        cursor.execute(query, data)

        # Make sure data is committed to the database
        connection.commit()
        last_row_id = cursor.lastrowid

        return last_row_id

    except Exception as err:
            print(f'The error while performing sql query for insert/update of product: {err}')
    finally:
        cursor.close()


def delete_product(connection, product_id):
    cursor = connection.cursor()
    try:
        query = ("DELETE FROM products where product_id=" + str(product_id))
        cursor.execute(query)

        # Make sure data is committed to the database
        connection.commit()
    except Exception as err:
        print(f'The error while performing sql query for deletion of product: {err}')
    finally:
        cursor.close()


# making the code modular
if __name__ == "__main__":
    connection = get_sql_connection()
    if connection is not None:
        print(get_all_products(connection))
       #  print(delete_product(g.db_conn, 3))


"""        print(insert_new_product(g.db_conn, {
            'product_name': 'cabbage',
            'uom_id': '1',
            'price_per_unit': '10'
        }))"""