from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from ..models import db, Item, Location

bp = Blueprint('inventories', __name__, url_prefix='/v1/locations')


@bp.route('<int:locId>/inventories', methods=['GET'])
def get_all_items(locId):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    location = Location.query.filter_by(id = locId).first()
    output = []

    for item in location.items:
        item_data = {}
        item_data['name'] = item.name
        item_data['amount'] = item.amount
        output.append(item_data)

    return jsonify({'items' : output}), 200


@bp.route('<int:locId>/inventories/<string:itemName>', methods=['GET'])
def get_amount_of_item(locId, itemName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    get_item = Item.query.filter_by(location_id = locId, name = itemName).first()

    if not get_item:
        return jsonify({'code' : '404', 'message' : 'Item not in inventory', 'description' : 'This item is not located in this inventory'}), 404

    return jsonify({'amount' : get_item.amount}), 200


@bp.route('<int:locId>/inventories/<string:itemName>', methods=['PUT'])
def update_item_amount(locId, itemName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    if not request.data:
        return jsonify({'code' : '400', 'message' : 'No JSON','description' : 'Expected a JSON object'}), 400

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'}), 400
    
    if not 'itemAmount' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing item name or amount'}), 400
    
    get_item = Item.query.filter_by(location_id = locId, name = itemName).first()
    if not get_item:
        return jsonify({'code' : '404', 'message' : 'Item not in inventory', 'description' : 'This item is not located in this inventory'}), 404
    
    get_item.amount = data['itemAmount']
    db.session.commit()

    return jsonify({'code' : '204', 'message' : 'Item updated','description' : 'The item has successfully been updated'}),204


@bp.route('<int:locId>/inventories', methods=['POST'])
def create_new_item(locId):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    if not request.data:
        return jsonify({'code' : '400', 'message' : 'No JSON','description' : 'Expected a JSON object'}), 400

    if not request.content_type == 'application/json':
        return jsonify({'code' : '400', 'message' : 'Expected JSON','description' : 'POST method expected a JSON in application/json'}), 400

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'}), 400


    if not 'itemName' in data or not 'itemAmount' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing item name or amount'}), 400


    location = Location.query.filter_by(id=locId).first()
    for item in location.items:
        if data['itemName'] == item.name:
            return jsonify({'code' : '304', 'message' : 'New item not created', 'description' : 'The requested item is already in the database'}), 304


    new_item = Item(name=data['itemName'], amount=data['itemAmount'], location_id = locId)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New item created', 'description' : 'An item has successfully been created'}), 201


@bp.route('<int:locId>/inventories/<string:itemName>', methods=['DELETE'])
def delete_item(locId, itemName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    get_item = Item.query.filter_by(location_id = locId, name = itemName).first()

    if not get_item:
        return jsonify({'code' : '404', 'message' : 'Item not in inventory', 'description' : 'This item is not located in this inventory'}), 404
    else:
        db.session.delete(get_item)
        db.session.commit()
        return jsonify({'code' : '204', 'message' : 'No Content', 'description' : 'An item has successfully been deleted'}), 204