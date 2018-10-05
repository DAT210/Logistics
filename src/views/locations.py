from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from ..models import db, Location

bp = Blueprint('locations', __name__, url_prefix='/v1/locations')

@bp.route('', methods=['GET'])
def get_all_locations():

    locations = Location.query.order_by(Location.id).all()
    output = []

    for location in locations:
        location_data = {}
        location_data['id'] = location.id
        location_data['name'] = location.name
        output.append(location_data)

    return jsonify({'locations' : output}), 200


@bp.route('<int:locId>', methods=['GET'])
def get_name_of_location(locId):
    get_location = Location.query.filter_by(id = locId).first()
    if not get_location:
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    return jsonify({'id' : get_location.id, 'name' : get_location.name}), 200


@bp.route('<int:locId>', methods=['PUT'])
def update_location_name(locId):
    get_location = Location.query.filter_by(id = locId).first()
    if not get_location:
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    if not request.data:
        return jsonify({'code' : '400', 'message' : 'No JSON','description' : 'Expected a JSON object'}), 400

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'}), 400
    
    if not 'locationName' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing location name'}), 400
    
    get_location.name = data['locationName']
    db.session.commit()

    return jsonify({'code' : '204', 'message' : 'Location updated','description' : 'The location has successfully been updated'}),204


@bp.route('', methods=['POST'])
def create_new_location():
    if not request.data:
        return jsonify({'code' : '400', 'message' : 'No JSON','description' : 'Expected a JSON object'}), 400

    if not request.content_type == 'application/json':
        return jsonify({'code' : '400', 'message' : 'Expected JSON','description' : 'POST method expected a JSON in application/json'}), 400

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'}), 400


    if not 'locationName' in data:
        return jsonify({'code' : '400', 'message' : 'Not enough data', 'description' : 'Missing location name'}), 400

    new_location = Location(name=data['locationName'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New location created', 'description' : 'A location has successfully been created'}), 201


@bp.route('<int:locId>', methods=['DELETE'])
def delete_location(locId):
    get_location = Location.query.filter_by(id = locId).first()

    if not get_location:
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404
    else:
        db.session.delete(get_location)
        db.session.commit()
        return jsonify({'code' : '204', 'message' : 'No Content', 'description' : 'An location has successfully been deleted'}), 204
