from models.model_mixin import MixinModel
from db import BaseModel, db


class CategoryModel(BaseModel, MixinModel):
    __tablename__ = "categories"  # Name of the database table

    # Setting an ID for each product
    id = db.Column(db.Integer, primary_key=True)

    categoryName = db.Column(db.String(80))

    def json(self):
        return {"categoryName": self.categoryName}

    def __init__(self, categoryName):
        self.categoryName = categoryName
