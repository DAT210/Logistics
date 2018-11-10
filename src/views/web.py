from flask import Blueprint, current_app, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests, json
from flask_jwt_extended import jwt_required
bp = Blueprint('web', __name__, url_prefix="/locations")


@bp.route("/", methods=['GET'])
def locations():
    token = request.cookies.get('access_token_cookie')
    if token == None:
        return redirect('/locations/login')
    valid_token = requests.get("https://logistics_app:5000/v1/locations/auth", headers={'Authorization' : "Bearer " + token}, timeout=10, verify=False)
    if valid_token.status_code == 200:
        response = requests.get("https://logistics_app:5000/v1/locations/", headers={'Authorization' : "Bearer " + token}, timeout=10, verify=False)
        return render_template('locations.html', locations=response.json()['locations'])
    return redirect('/locations/login')

@bp.route("/<int:locId>", methods=['GET'])
def ingredients(locId):
    token = request.cookies.get('access_token_cookie')
    if token == None:
        return redirect('/locations/login')
    valid_token = requests.get("https://logistics_app:5000/v1/locations/auth", headers={'Authorization' : "Bearer " + token}, timeout=10, verify=False)
    if valid_token.status_code == 200:
        response = requests.get("https://logistics_app:5000/v1/locations/" + str(locId) + "/ingredients", headers={'Authorization' : "Bearer " + token}, timeout=10, verify=False)
        location = requests.get("https://logistics_app:5000/v1/locations/" + str(locId), headers={'Authorization' : "Bearer " + token}, timeout=10, verify=False)
        return render_template('ingredients.html', ingredients=response.json()['ingredients'], location=location.json())
    return redirect('/locations/login')
    
@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
