from crypt import methods
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

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


@app.route('/ping', )
def ping():
    return jsonify({'message': 'Pingeado'})


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products/<string:name>')
def get_product(name):

    productFound = [product for product in products if product['name'] == name]
    if (len(productFound) == 0):
        return jsonify({'message': 'Product not found'})
    return jsonify(productFound)


@app.route('/products', methods=['POST'])
def create_product():

    newProduct = {
        'name': request.json['name'],
        'price': request.json['price'],
        'stock': request.json['stock']
    }

    products.append(newProduct)

    return jsonify(products)


@app.route('/products/<string:name>', methods=['PUT'])
def update_product(name):

    productFound = [product for product in products if product['name'] == name]

    if len(productFound) == 0:
        return jsonify({'message': 'Product not found'})

    if len(productFound) > 1:
        for p in productFound:
            p['name'] = request.json['name']
            p['price'] = request.json['price']
            p['stock'] = request.json['stock']

    return jsonify(products)


@app.route('/products/<string:name>', methods=['DELETE'])
def delete_product(name):

    productFound = [product for product in products if product['name'] == name]

    if len(productFound) == 0:
        return jsonify({'message': 'Product not found'})

    for p in productFound:
        products.remove(p)

    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)
