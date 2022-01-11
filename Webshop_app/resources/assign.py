from flask_restful import Resource, reqparse
from models.product import ProductModel
from models.category import CategoryModel
from models.category_link import CategoryLink
from db import db


class AssignProductToCategory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('category_id',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = AssignProductToCategory.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404
        category = CategoryModel.find_by_attribute(id=data["category_id"])
        if not category:
            return {"message": "This category does not exist"}, 404

        if CategoryLink.find_by_attribute(product_id=data["product_id"], category_id=data["category_id"]):
            return {"message": f"{product.productName} is already in {category.categoryName} category!"}, 200

        link = CategoryLink(**data)
        link.save_to_db()
        return {"message": f"{product.productName} is assigned to {category.categoryName} successfully!"}, 201
