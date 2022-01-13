from flask import Flask
from flask_restful import Api
from Webshop_app.db import db
from os import environ, path, mkdir

from flask_jwt import JWT

# Resources
from Webshop_app.resources.user import UserRegister
from Webshop_app.resources.category import Category, CategoryManagement
from Webshop_app.resources.product import Product, ProductManagement
from Webshop_app.resources.assign import AssignProductToCategory

from Webshop_app.security import authenticate, identity

# App config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = environ.get('SECRET_KEY')

api = Api(app)  # Creating an instance of the Api class

db.init_app(app)  # Connecting app to database


@app.before_first_request  # Create all tables on first request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # Creating JWT instance


@app.route("/")
def index():
    return "Hello"


api.add_resource(UserRegister, "/register")
api.add_resource(Category, "/categories")
api.add_resource(CategoryManagement, "/categories/<int:category_id>")
api.add_resource(Product, "/products")
api.add_resource(ProductManagement, "/products/<string:productName>")
api.add_resource(AssignProductToCategory, "/assign")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debuf=True)
