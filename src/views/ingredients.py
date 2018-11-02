from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from ..models import db, Ingredient, Location
from .locations import token_required
import os

bp = Blueprint('ingredients', __name__, url_prefix='/v1/locations/')



# Route to get every ingredient in the inventory of the specified location
@bp.route('<int:locId>/ingredients', methods=['GET'])
@token_required
def get_all_ingredients(current_user, locId):
    # Check if location exists in the database, this test is in every route
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    location = Location.query.filter_by(id = locId).first()
    output = []

    for ingredient in location.ingredients:
        ingredient_data = {}
        ingredient_data['name'] = ingredient.name
        ingredient_data['amount'] = ingredient.amount
        output.append(ingredient_data)

    return jsonify({'ingredients' : output}), 200


# Route to get a specific ingredient in the inventory of a location
@bp.route('<int:locId>/ingredients/<string:ingredientName>', methods=['GET'])
@token_required
def get_amount_of_ingredient(current_user, locId, ingredientName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    get_ingredient = Ingredient.query.filter_by(location_id = locId, name = ingredientName.capitalize()).first()

    if not get_ingredient:
        return jsonify({'code' : '404', 'message' : 'ingredient not in inventory', 'description' : 'This ingredient is not located in this inventory'}), 404

    return jsonify({'amount' : get_ingredient.amount, 'name' : get_ingredient.name}), 200


# Route to update a ingredient by adding or subtracting the amount
@bp.route('<int:locId>/ingredients/<string:ingredientName>', methods=['PUT'])
@token_required
def update_ingredient_amount(current_user, locId, ingredientName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404
    
    # Check if there is data in the request
    if not request.data:
        return jsonify({'code' : '400', 'message' : 'No JSON','description' : 'Expected a JSON object'}), 400

    # If there is data in the request, then try to decode the json.
    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'}), 400
    
    # Check if the names are correct in the json input, and if they exist
    if not 'ingredientAmount' in data or not 'action' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing amount or action'}), 400
    
    # Check if ingredientAmount is a int
    if not isinstance(data['ingredientAmount'], int):
        return jsonify({'code' : '400', 'message' : 'Bad input', 'description' : 'Amount needs to be an integer'}), 400

    get_ingredient = Ingredient.query.filter_by(location_id = locId, name = ingredientName.capitalize()).first()
    # Check if the ingredient exists in the inventory
    if not get_ingredient:
        return jsonify({'code' : '404', 'message' : 'ingredient not in inventory', 'description' : 'This ingredient is not located in this inventory'}), 404
    
    if data['action'] == 'add':
        get_ingredient.amount = get_ingredient.amount + data['ingredientAmount']

    elif data['action'] == 'subtract':
        amount = get_ingredient.amount - data['ingredientAmount']
        if amount <= 5:
            # Refills the specified item, but still sends 
            if os.environ.get('AUTO_REFILL'):
                get_ingredient.amount = get_ingredient.amount + 50
                db.session.commit()
                return jsonify({'code' : '400', 'message' : 'Not enough of ingredients, refills', 
        'description' : 'Trying to reduce the amount of an ingredient causes the amount to become negative, but it is refilling the storage'}), 400 

            else:
                return jsonify({'code' : '400', 'message' : 'Not enough of ingredients', 
        'description' : 'Trying to reduce the amount of an ingredient causes the amount to become negative'}), 400 
        get_ingredient.amount = amount
    
    else:
        return jsonify({'code' : '400', 'message' : 'Invalid action', 'description' : 'Uknown action in input'}), 400

    db.session.commit()

    return jsonify({'code' : '204', 'message' : 'ingredient updated','description' : 'The ingredient has successfully been updated'}),204


# Route to add new ingredient to the inventory
@bp.route('<int:locId>/ingredients', methods=['POST'])
@token_required
def create_new_ingredient(current_user, locId):
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


    if not 'ingredientName' in data or not 'ingredientAmount' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing ingredient name or amount'}), 400

    if not isinstance(data['ingredientAmount'], int):
        return jsonify({'code' : '400', 'message' : 'Bad input', 'description' : 'Amount needs to be an integer'}), 400

    location = Location.query.filter_by(id=locId).first()
    for ingredient in location.ingredients:
        if data['ingredientName'] == ingredient.name:
            return jsonify({'code' : '304', 'message' : 'New ingredient not created', 'description' : 'The requested ingredient is already in the database'}), 304


    new_ingredient = Ingredient(name=data['ingredientName'].capitalize(), amount=data['ingredientAmount'], location_id = locId)
    db.session.add(new_ingredient)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New ingredient created', 'description' : 'An ingredient has successfully been created'}), 201


# Route to delete a ingredient from the inventory
@bp.route('<int:locId>/ingredients/<string:ingredientName>', methods=['DELETE'])
@token_required
def delete_ingredient(current_user, locId, ingredientName):
    if not Location.query.filter_by(id=locId).first():
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    get_ingredient = Ingredient.query.filter_by(location_id = locId, name = ingredientName.capitalize()).first()

    if not get_ingredient:
        return jsonify({'code' : '404', 'message' : 'ingredient not in inventory', 'description' : 'This ingredient is not located in this inventory'}), 404
    else:
        db.session.delete(get_ingredient)
        db.session.commit()
        return jsonify({'code' : '204', 'message' : 'No Content', 'description' : 'An ingredient has successfully been deleted'}), 204
