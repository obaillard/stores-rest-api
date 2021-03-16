from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    """
    Item class
    """

    # define class method
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    # like @app.route('/item/<string:name>')
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'message': f'Item "{name}" cannot be found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item "{name}" already exists.'}, 400

        # Get arguments from JSON
        data = Item.parser.parse_args()

        # Create item in DB
        item = ItemModel(name, **data)

        # Insert item in DB
        try:
            item.save_to_db()
        except:
            return {'message', 'An error occurred inserting the item.'}, 500  # 500: internal server error

        return item.json(), 201  # 201: created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.store_id = data['store_id']
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    """
    ItemList class
    """
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
