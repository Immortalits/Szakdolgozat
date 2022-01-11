from flask_restful import Resource, reqparse
from sqlalchemy.orm import query
from models.product import ProductModel

minLength = 3  # Minimum length of the product names.


class Product(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('productName',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('availability',
                        type=bool,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('description',
                        type=str,
                        required=False,
                        # help="This field cannot be blank."
                        )

    def post(self):
        data = Product.parser.parse_args()
        if len(data['productName'].strip()) > minLength and int(data["price"]) > 0:
            if ProductModel.find_by_attribute(productName=data['productName']):
                return {"message": f"A product with {data['productName']} name already exists"}, 400

            desc = ""
            if data['description']:
                desc = data['description']
            else:
                desc = "Missing description!"

            product = ProductModel(data['productName'].strip(), int(
                data['price']), data['availability'], desc)
            product.save_to_db()

            return {"message": "Product created successfully."}, 201
        else:
            return {"message": f"Please give a valid product name of at least {minLength} characters!"}

    def get(self):
        return {
            "products": [product.json() for product in ProductModel.query.all()]
        }
