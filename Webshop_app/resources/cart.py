from flask_restful import Resource, reqparse
from Webshop_app.models.product import ProductModel
from Webshop_app.models.user import UserModel
from Webshop_app.models.cart import CartModel
from Webshop_app.models.cart_link import CartLink
from Webshop_app.db import db
from flask_jwt import jwt_required


class AssignProductToCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('amount',
                        type=int,
                        required=False)

    def post(self, user_id):
        data = AssignProductToCart.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404
        user = UserModel.find_by_attribute(id=data["user_id"])
        if not user:
            return {"message": "This user does not exist"}, 404

        if data['amount'] and data['amount'] >= 1:
            amount = data['amount']
        else:
            # if no amount is defined
            amount = 1

        if CartModel.find_by_attribute(user_id=data["user_id"]):
            cart = CartModel.find_by_attribute(user_id=data["user_id"])

            if CartLink.find_by_attribute(cart_id=cart.id, product_id=data["product_id"]):
                cartLink = CartLink.find_by_attribute(
                    cart_id=cart.id, product_id=data["product_id"])
                var = cartLink.amount + amount
                if var >= 0:
                    cartLink.amount += amount
                elif var < 0:
                    return {"message": f"{product.productName} has been reduced by {abs(amount)}."}, 200
                else:
                    cartLink.delete_from_db()
                    return {"message": f"{product.productName} has been removed from cart."}, 200

                cartLink.save_to_db()
                return {"message": f"{product.productName} has been increased by {amount}."}, 200
            else:
                cartLink = CartLink(data['product_id'], cart.id)
                cartLink.amount = amount
                cartLink.save_to_db()

                return {"message": f"{product.productName} has been added to cart."}, 200

        return {"message": f"User does not have a cart, please contact the support!"}, 200

    # @jwt_required()
    def get(self, user_id):  # /user_id/cart
        cart = CartModel.find_by_attribute(user_id=user_id)
        return {
            "Cart": list(map(lambda product: product.json(), CartModel.query.filter_by(id=cart.id)))
        }

    def put(self, user_id):
        data = AssignProductToCart.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404
        user = UserModel.find_by_attribute(id=data["user_id"])
        if not user:
            return {"message": "This user does not exist"}, 404

        if data['amount'] and data['amount'] >= 1:
            amount = data['amount']
        else:
            # if no amount is defined
            amount = 1

        if CartModel.find_by_attribute(user_id=data["user_id"]):
            cart = CartModel.find_by_attribute(user_id=data["user_id"])

            if CartLink.find_by_attribute(cart_id=cart.id, product_id=data["product_id"]):
                cartLink = CartLink.find_by_attribute(
                    cart_id=cart.id, product_id=data["product_id"])
                var = cartLink.amount = amount

                cartLink.save_to_db()
                return {"message": f"{product.productName} has been changed to {amount}."}, 200
            else:
                cartLink = CartLink(data['product_id'], cart.id)
                cartLink.amount = amount
                cartLink.save_to_db()

                return {"message": f"{product.productName} has been added to cart."}, 200

        return {"message": f"User does not have a cart, please contact the support!"}, 200

    def delete(self, user_id):
        data = AssignProductToCart.parser.parse_args()

        product = ProductModel.find_by_attribute(id=data["product_id"])
        if not product:
            return {"message": "This product does not exists"}, 404
        user = UserModel.find_by_attribute(id=data["user_id"])
        if not user:
            return {"message": "This user does not exist"}, 404

        if CartModel.find_by_attribute(user_id=data["user_id"]):
            cart = CartModel.find_by_attribute(user_id=data["user_id"])

            if CartLink.find_by_attribute(cart_id=cart.id, product_id=data["product_id"]):
                cartLink = CartLink.find_by_attribute(
                    cart_id=cart.id, product_id=data["product_id"])

                cartLink.delete_from_db()
                return {"message": f"{product.productName} has been removed from the cart."}, 200
            else:
                return {"message": f"{product.productName} is not in the cart."}, 200

        return {"message": f"User does not have a cart, please contact the support!"}, 200
