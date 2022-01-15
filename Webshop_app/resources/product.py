from flask_restful import Resource, reqparse
from Webshop_app.models.product import ProductModel


# Minimum length of the product names.
minLength = 3


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


class ProductManagement(Resource):

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

    def delete(self, productName):
        product = ProductModel.find_by_attribute(productName=productName)
        if product:
            product.delete_from_db()
            return {"message": f"{productName} product has been deleted successfully."}
        return {"message": f"Product with name: {productName} does not exists!"}

    def put(self, productName):

        data = ProductManagement.parser.parse_args()

        if len(data['productName'].strip()) > minLength and int(data["price"]) > 0:

            product = ProductModel.find_by_attribute(
                productName=productName)
            if product:
                product.productName = data["productName"]
                product.price = data["price"]
                product.availability = bool(data["availability"])

                desc = ""
                if data['description']:
                    desc = data['description']
                else:
                    desc = "Missing description!"

                product.description = desc
                product.save_to_db()

                return {"message": f"{productName} product has been updated to {data['productName']} successfully."}

            return {"message": f"Product with name: {productName} does not exists!"}
        else:
            return {"message": f"Please give a valid product name of at least {minLength} characters!"}
