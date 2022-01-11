from models.model_mixin import MixinModel
from db import BaseModel, db


class ProductModel(BaseModel, MixinModel):
    __tablename__ = "products"  # Name of the database table

    # Setting an ID for each product
    id = db.Column(db.Integer, primary_key=True)

    productName = db.Column(db.String(80))
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    description = db.Column(db.Text)

    def json(self):
        data = {
            "productName": self.productName,
            "price": self.price,
            "availability": self.availability,
            "description": self.description
        }

        return data

    def __init__(self, productName, price, availability, description=""):
        self.productName = productName
        self.price = price
        self.availability = availability
        self.description = description
