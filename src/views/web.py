from flask import Blueprint, current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from ..models import db, Location, Ingredient
import requests, json, base64
bp = Blueprint('web', __name__, url_prefix="/locations")


@bp.route("/", methods=['GET'])
def locations():
    headers = {'Authorization' : 'Basic {}'.format(base64.b64encode(b'admin:password').decode('utf8'))}
    token = requests.get("https://logistics_app:5000/v1/locations/login", headers=headers, verify=False)
    
    response = requests.get("https://logistics_app:5000/v1/locations/", headers={'Authorization' : "Bearer " + token.json()['access_token']}, timeout=10, verify=False)
    return render_template('locations.html', locations=response.json()['locations'])

@bp.route("/<int:locId>", methods=['GET'])
def ingredients(locId):
    headers = {'Authorization' : 'Basic {}'.format(base64.b64encode(b'admin:password').decode('utf8'))}
    token = requests.get("https://logistics_app:5000/v1/locations/login", headers=headers, verify=False)
    
    response = requests.get("https://logistics_app:5000/v1/locations/" + str(locId) + "/ingredients", headers={'Authorization' : "Bearer " + token.json()['access_token']}, timeout=10, verify=False)
    location = requests.get("https://logistics_app:5000/v1/locations/" + str(locId), headers={'Authorization' : "Bearer " + token.json()['access_token']}, timeout=10, verify=False)
    return render_template('ingredients.html', ingredients=response.json()['ingredients'], location=location.json())
    
@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
