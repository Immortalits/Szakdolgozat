from flask_restful import Resource, reqparse
from sqlalchemy.orm import query
from Webshop_app.models.category import CategoryModel

minLength = 3  # Minimum length of the category names.


class Category(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('categoryName',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = Category.parser.parse_args()
        if len(data['categoryName'].strip()) > minLength:
            if CategoryModel.find_by_attribute(categoryName=data['categoryName']):
                return {"message": f"A category with {data['categoryName']} name already exists"}, 400
            category = CategoryModel(data['categoryName'].strip())
            category.save_to_db()

            return {"message": "Category created successfully."}, 201
        else:
            return {"message": f"Please give a valid category name of at least {minLength} characters!"}

    def get(self):
        return {
            "categories": [category.json(assigned=False) for category in CategoryModel.query.all()]
        }


class CategoryManagement(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('categoryName',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def delete(self, categoryName):
        category = CategoryModel.find_by_attribute(categoryName=categoryName)
        if category:
            category.delete_from_db()
            return {"message": f"{categoryName} category has been deleted successfully."}
        return {"message": f"Category with name: {categoryName} does not exists!"}

    def put(self, categoryName):

        data = CategoryManagement.parser.parse_args()

        if len(data['categoryName'].strip()) > minLength:

            category = CategoryModel.find_by_attribute(
                categoryName=categoryName)
            if category:
                category.categoryName = data["categoryName"]
                category.save_to_db()
                return {"message": f"{categoryName} category has been updated to {data['categoryName']} successfully."}
            return {"message": f"Category with name: {categoryName} does not exists!"}
        else:
            return {"message": f"Please give a valid category name of at least {minLength} characters!"}

    def get(self, categoryName):
        return {
            categoryName: list(
                map(lambda product: product.json(), CategoryModel.query.filter_by(categoryName=categoryName)))
        }
