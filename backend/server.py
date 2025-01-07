# basic boiler plater code for flask
import json

from flask import Flask, request, jsonify, g
from sql_connection import get_sql_pool

import products_dao
import uom_dao
import order_dao

app = Flask(__name__)


# As soon the server is live, the connection is made to the database
# This is the global connection that will be reused in subsequent calls as it's created outside the handler.
# Once closed, this global connection can't be reused, and any further operations throw an error.

# Flask handles requests in isolation, and the same global connection might be shared by multiple threads,
# causing concurrency issues.
db_pool = get_sql_pool()


# Creating hooks that will be called before and after each request
@app.before_request
def get_db_connection():
    # Get a connection from the pool
    g.db_conn = db_pool.get_connection()


@app.teardown_request
def release_db_connection(exception):
    # Close (return) the connection to the pool
    if hasattr(g, 'db_conn'):
        g.db_conn.close()


@app.route('/getProducts', methods=['GET'])
def get_products():
    products = products_dao.get_all_products(g.db_conn)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(g.db_conn, request.form["product_id"])
    response = jsonify({
        "product_id": return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getUOM', methods=['GET'])
def get_uom():
    uom = uom_dao.get_uoms(g.db_conn)
    response = jsonify(uom)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(g.db_conn, request_payload )
    response = jsonify({
        "product_id": product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order_dao.insert_new_order(g.db_conn, request_payload)
    response = jsonify({
        "order_id": order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    orders = order_dao.get_all_orders(g.db_conn)
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getOrderDetails', methods=['POST'])
def get_order_details():

    order_id = request.form.get('order_id')
    orders = order_dao.get_order_details(g.db_conn, order_id)
    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteOrder', methods=['POST'])
def delete_order():
    return_id = order_dao.delete_order(g.db_conn, request.form["order_id"])
    response = jsonify({
        "order_id": return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Staring Python flask server for grocery store management system")
    app.run(port=5000)
