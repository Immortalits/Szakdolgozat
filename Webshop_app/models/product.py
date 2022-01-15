from Webshop_app.models.model_mixin import MixinModel
from Webshop_app.db import BaseModel, db
from Webshop_app.models.cart_link import CartLink


class ProductModel(BaseModel, MixinModel):
    __tablename__ = "products"  # Name of the database table

    # Setting an ID for each product
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(80))
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    description = db.Column(db.Text)

    # Relationships
    categories = db.relationship('CategoryLink', back_populates='product')
    carts = db.relationship('CartLink', back_populates='product')

    def json(self, full=True):
        if full:
            data = {
                "productName": self.productName,
                "price": self.price,
                "availability": self.availability,
                "description": self.description
            }
        else:
            data = self.productName

        return data

    def __init__(self, productName, price, availability, description=""):
        self.productName = productName
        self.price = price
        self.availability = availability
        self.description = description
