from models.model_mixin import MixinModel
from db import BaseModel, db
from models.category_link import CategoryLink


class CategoryModel(BaseModel, MixinModel):
    __tablename__ = "categories"  # Name of the database table

    # Setting an ID for each product
    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(80))

    # Relationship
    products = db.relationship(CategoryLink, back_populates='category')

    def json(self, assigned=True):
        category = {"categoryName": self.categoryName}
        if assigned:
            products = []
            for link in self.products:
                if link.product is not None:
                    products.append(link.product.json(full=False))
            category = {'products': products}

        return category

    def __init__(self, categoryName):
        self.categoryName = categoryName
