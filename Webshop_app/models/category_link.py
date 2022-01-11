# https: // flask-sqlalchemy.palletsprojects.com/en/2.x/models/


from Webshop_app.models.model_mixin import MixinModel
from Webshop_app.db import BaseModel, db


class CategoryLink(BaseModel, MixinModel):
    __tablename__ = 'product_category'
    product_id = db.Column(db.ForeignKey('products.id'), primary_key=True)
    category_id = db.Column(db.ForeignKey('categories.id'), primary_key=True)
    product = db.relationship('ProductModel', back_populates='categories')
    category = db.relationship('CategoryModel', back_populates='products')

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id
