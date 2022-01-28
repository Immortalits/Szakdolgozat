from flask_restful import Resource, reqparse
from Webshop_app.models.user import UserModel
from Webshop_app.security import hash_password
from Webshop_app.models.cart import CartModel
from flask_jwt import jwt_required


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
    parser.add_argument('password_again',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_attribute(username=data['username']):
            return {"message": "A user with that username already exists"}, 400
        if data["password"] != data["password_again"]:
            return {"message": "Passwords must match!"}, 400

        user = UserModel(data['username'], hash_password(data['password']))
        user.save_to_db()

        cart = CartModel(user.id)
        cart.save_to_db()

        return {"message": "User created successfully."}, 201


class GetUsers(Resource):
    def get(self):
        return {
            "users": [user.username for user in UserModel.query.all()]
        }


class UserManagement(Resource):
    # /users/<int:user_id>
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=False,
                        help="This field cannot be blank.")
    parser.add_argument('new_password',
                        type=str,
                        required=False,
                        help="This field cannot be blank.")
    parser.add_argument('new_password_again',
                        type=str,
                        required=False,
                        help="This field cannot be blank.")

    def put(self, user_id):

        data = UserManagement.parser.parse_args()

        if UserModel.find_by_attribute(id=user_id):
            user = UserModel.find_by_attribute(id=user_id)

            prevUsername = user.username
            if data["new_password"] and data["new_password"] != "":
                if data["new_password"] == data["new_password_again"]:
                    if user.password == hash_password(data["password"]):
                        user.password = hash_password(data["new_password"])
                        user.save_to_db()
                        return {"message": "Password has been updates successfully!"}, 200
                    else:
                        return {"message": "Please provide your current password!"}, 400
                else:
                    return {"message": "Passwords must match!"}, 400
            else:
                user.username = data["username"]
                user.save_to_db()

                return {"message": f"{prevUsername} has been updated to {data['username']}"}, 200

        return {"message": "User was not found!"}, 404

    @jwt_required()
    def delete(self, user_id):
        if UserModel.find_by_attribute(id=user_id):
            user = UserModel.find_by_attribute(id=user_id)
            user.delete_from_db()

            return {"message": f"{user.username} has been deletedsuccesfully!"}, 200

        return {"message": "User was not found!"}, 404
