from flask_restful import Resource, reqparse
from Webshop_app.models.user import UserModel
from Webshop_app.security import hash_password
from Webshop_app.models.cart import CartModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_attribute(username=data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], hash_password(data['password']))
        user.save_to_db()

        cart = CartModel(user.id)
        cart.save_to_db()

        return {"message": "User created successfully."}, 201
