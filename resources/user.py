from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name='username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument(name='password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        # Parse request
        data = UserRegister.parser.parse_args()

        # check if user exist
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exits'}, 400  # 400: Bad request

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User successfully created.'}, 201   # 201: created
