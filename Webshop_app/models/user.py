from Webshop_app.models.model_mixin import MixinModel
from Webshop_app.db import BaseModel, db
from Webshop_app.models.cart import CartModel


class UserModel(BaseModel, MixinModel):
    __tablename__ = "users"  # Name of the database table

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # Relationships
    cart = db.relationship(CartModel, back_populates="user", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
