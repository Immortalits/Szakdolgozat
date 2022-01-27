from flask_restful import Resource, reqparse
from Webshop_app.models.product import ProductModel
from Webshop_app.models.category import CategoryModel
from Webshop_app.models.category_link import CategoryLink
from Webshop_app.db import db


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
        self.parser.remove_argument("new_category_id")
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

    def put(self):
        self.parser.add_argument('new_category_id',
                                 type=str,
                                 required=False,
                                 help="This field cannot be blank.")

        data = AssignProductToCategory.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404
        category = CategoryModel.find_by_attribute(id=data["category_id"])
        if not category:
            return {"message": "This category does not exist"}, 404

        if CategoryLink.find_by_attribute(product_id=data["product_id"], category_id=data["new_category_id"]):
            return {"message": f"{product.productName} is already in this category!"}

        if CategoryLink.find_by_attribute(product_id=data["product_id"], category_id=data["category_id"]):
            link = CategoryLink.find_by_attribute(
                product_id=data["product_id"], category_id=data["category_id"])

            link.category_id = data["new_category_id"]
            link.save_to_db()

            new_category = CategoryModel.find_by_attribute(
                id=data["new_category_id"])

            return {"message": f"{product.productName} has been assigned to {new_category.categoryName} from {category.categoryName} successfully!"}, 201

    def delete(self):
        self.parser.remove_argument("new_category_id")
        data = AssignProductToCategory.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404

        category = CategoryModel.find_by_attribute(id=data["category_id"])
        if not category:
            return {"message": "This category does not exist"}, 404

        if CategoryLink.find_by_attribute(product_id=data["product_id"], category_id=data["category_id"]):

            link = CategoryLink.find_by_attribute(
                product_id=data["product_id"], category_id=data["category_id"])
            link.delete_from_db()

            return {"message": f"{product.productName} was removed from {category.categoryName} category!"}, 200

        return {"message": "This assignment does not exist!"}
