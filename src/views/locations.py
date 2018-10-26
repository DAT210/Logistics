from flask import Flask, request, jsonify, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from ..models import db, Location
import jwt, datetime, os
from functools import wraps

bp = Blueprint('locations', __name__, url_prefix='/v1/locations/')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'code' : '403', 'message' : 'Missing token', 'description' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            # This is a test, should be more secure when implementing it completely
            if os.environ.get('INV_JWT_USER') == data['username']:
                current_user = data['username']
        except:
            return jsonify({'code' : '403', 'message' : 'Invalid', 'description' : 'Token is invalid'}), 403
        
        return f(current_user, *args, **kwargs)
    return decorated


# Route to get all locations
@bp.route('', methods=['GET'])
@token_required
def get_all_locations(current_user):

    locations = Location.query.order_by(Location.id).all()
    output = []

    for location in locations:
        location_data = {}
        location_data['id'] = location.id
        location_data['name'] = location.name
        output.append(location_data)

    return jsonify({'locations' : output}), 200


# Route to get information about a specific location
@bp.route('<int:locId>', methods=['GET'])
@token_required
def get_name_of_location(current_user, locId):
    get_location = Location.query.filter_by(id = locId).first()
    if not get_location:
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404

    return jsonify({'id' : get_location.id, 'name' : get_location.name}), 200


# Route to update the name of a location
@bp.route('<int:locId>', methods=['PUT'])
@token_required
def update_location_name(current_user, locId):
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


# Route to add a new location
@bp.route('', methods=['POST'])
@token_required
def create_new_location(current_user):
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


# Route to delete a location
@bp.route('<int:locId>', methods=['DELETE'])
@token_required
def delete_location(current_user, locId):
    get_location = Location.query.filter_by(id = locId).first()

    if not get_location:
        return jsonify({'code' : '404', 'message' : 'Location does not exist', 'description' : 'This location does not exist in the database'}), 404
    else:
        for ingredient in get_location.ingredients:
            db.session.delete(ingredient)
        db.session.delete(get_location)
        db.session.commit()
        return jsonify({'code' : '204', 'message' : 'No Content', 'description' : 'An location has successfully been deleted'}), 204


# Route to login and create a jwt token
@bp.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'code' : '401', 'message' : 'Unable to login', 'description' : 'Could not verify login'}), 401

    # Check username and password against the temporary user. Need to check with the employee database
    if auth.password == os.environ.get('INV_JWT_PASS') and auth.username == os.environ.get('INV_JWT_USER'):
        token = jwt.encode({'username' : os.environ.get('INV_JWT_USER'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token' : token.decode('UTF-8')})
    return jsonify({'code' : '401', 'message' : 'Unable to login', 'description' : 'Could not verify login'}), 401
