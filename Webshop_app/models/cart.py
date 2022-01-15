from Webshop_app.models.model_mixin import MixinModel
from Webshop_app.db import BaseModel, db
from Webshop_app.models.cart_link import CartLink


class CartModel(BaseModel, MixinModel):

    __tablename__ = 'carts'
    # Cart ID.
    id = db.Column(db.Integer, primary_key=True)
    # User ID link.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    purchased = db.Column(db.Boolean)

    # Relationships
    products = products = db.relationship(CartLink, back_populates='cart')

    user = db.relationship("UserModel", back_populates='cart')

    def __init__(self, user_id):
        self.user_id = user_id

    def json(self, assigned=True):
        cart = {"cartName": "Cart"}
        if assigned:
            products = []
            for link in self.products:
                if link.product is not None:
                    products.append(
                        [link.product.json(full=False), link.amount])
            cart = {'products': products}

        return cart
