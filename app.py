from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:mathenge,./1998@localhost/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marsh = Marshmallow(app)

# dbmodel creation


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float())
    qty = db.Column(db.Integer())

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# product schema

class ProductSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# init schema


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# create product route
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Products(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# get products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Products.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get one product


@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Products.query.get(id)
    return product_schema.jsonify(product)

# update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    updat = Products.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    updat.name = name
    updat.description = description
    updat.price = price
    updat.qty = qty

    db.session.commit()

    return product_schema.jsonify(updat)

# delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Products.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# run server


if __name__ == '__main__':
    app.run(debug=True)
