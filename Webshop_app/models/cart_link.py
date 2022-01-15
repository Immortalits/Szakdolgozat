from Webshop_app.models.model_mixin import MixinModel
from Webshop_app.db import BaseModel, db


class CartLink(BaseModel, MixinModel):
    __tablename__ = 'product_cart'

    product_id = db.Column(db.ForeignKey('products.id'), primary_key=True)
    cart_id = db.Column(db.ForeignKey('carts.id'), primary_key=True)
    amount = db.Column(db.Integer)

    # Relationships
    product = db.relationship('ProductModel', back_populates='carts')
    cart = db.relationship('CartModel', back_populates='products')

    def __init__(self, product_id, cart_id):
        self.product_id = product_id
        self.cart_id = cart_id
