from crypt import methods
from distutils.util import execute
import string
from unicodedata import name
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3

from products import products

app = Flask(__name__)

### Swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Products.API'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end Swagger specific ###


def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: string):
    conn = get_db_connection()
    dbresult = conn.execute(query).fetchall()
    conn.commit()
    conn.close()
    return dbresult


def map_to_product(dbresult):
    data = []
    for p in dbresult:
        data.append(
            {
                "name": p[0],
                "price": p[1],
                "stock": p[2]
            }
        )
    return data


@app.route('/ping', )
def ping():
    return jsonify({'message': 'Pingeado'})


@app.route('/products', methods=['GET'])
def get_products():
    dbproducts = execute_query('SELECT * FROM products')
    return jsonify(map_to_product(dbproducts))


@app.route('/products/<string:name>')
def get_product(name):
    dbproducts = execute_query(
        'SELECT * FROM products WHERE name LIKE "%' + name + '%"')
    data = map_to_product(dbproducts)
    if (len(dbproducts) == 0):
        return jsonify({'message': 'Product not found'})
    return jsonify(data)


@app.route('/products', methods=['POST'])
def create_product():
    execute_query(
        f"INSERT INTO Products (name, price, stock) VALUES('{request.json['name']}', {request.json['price']}, {request.json['stock']})")

    dbproducts = execute_query('SELECT * FROM products')
    return jsonify(map_to_product(dbproducts))


@app.route('/products/<string:name>', methods=['PUT'])
def update_product(name):
    execute_query(
        f"UPDATE Products SET name='{request.json['name']}', price={request.json['price']}, stock={request.json['stock']} WHERE name = '{name}'")

    dbproducts = execute_query('SELECT * FROM products')
    return jsonify(map_to_product(dbproducts))


@app.route('/products/<string:name>', methods=['DELETE'])
def delete_product(name):
    execute_query(
        f"DELETE FROM Products WHERE name='{name}'")
    
    dbproducts = execute_query('SELECT * FROM products')
    return jsonify(map_to_product(dbproducts))


if __name__ == '__main__':
    app.run(debug=True)
