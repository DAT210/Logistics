import sys
sys.path.append('../')
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Item, Location

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/locations/<int:locId>/inventories', methods=['GET'])
def get_all_items(locId):
    location = Location.query.filter_by(id = locId).first()
    output = []

    for item in location.items:
        item_data = {}
        item_data['name'] = item.name
        item_data['amount'] = item.amount
        output.append(item_data)

    resp = jsonify({'items' : output})
    resp.status_code = 200

    return resp


@app.route('/locations/<int:locId>/inventories/<string:itemName>', methods=['GET'])
def get_amount_of_item(locId, itemName):
    get_item = Item.query.filter_by(location_id = locId, name = itemName).first()

    if not get_item:
        resp = jsonify({'code' : '404', 'message' : 'Item not in inventory', 'description' : 'This item is not located in this inventory'})
        return resp, 404

    resp = jsonify({'amount' : get_item.amount})
    return resp, 200


@app.route('/locations/<int:locId>/inventories', methods=['PUT'])
def update_item_amount():
    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        resp = jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'})
        return resp, 400


    return ''


@app.route('/locations/<int:locId>/inventories', methods=['POST'])
def create_new_item(locId):
    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'})


    if not data['itemName'] or not data['itemAmount']:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing item name or amount'})


    location = Location.query.filter_by(id=locId).first()
    for item in location.items:
        if data['itemName'] == item.name:
            return jsonify({'code' : '1234', 'message' : 'New item not created', 'description' : 'The requested item is already in the database'})


    new_item = Item(name=data['itemName'], amount=data['itemAmount'], location_id = locId)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New item created', 'description' : 'An item has successfully been created'})


@app.route('/locations/<int:locId>/inventories/<string:itemName>', methods=['DELETE'])
def delete_group_items():
    return ''

if __name__ == '__main__':
    app.run(debug=True)