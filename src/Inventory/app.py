from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Integer)

@app.route('/inventories', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    output = []

    for item in items:
        item_data = {}
        item_data['name'] = item.name
        item_data['amount'] = item.amount
        output.append(item_data)

    return jsonify({'items' : output})

@app.route('/inventories/<itemNames>', methods=['GET'])
def get_group_items():
    return ''

@app.route('/inventories/<itemName>/<itemAmount>', methods=['PUT'])
def update_item_amount():
    return ''

@app.route('/inventories', methods=['POST'])
def create_new_item():

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return jsonify({'code' : '400', 'message' : 'Failed to decode','description' : 'Expected a JSON object'})

    test = Item.query.filter_by(name=data['itemName']).first()
    if test:
        return jsonify({'code' : '1234', 'message' : 'New item not created', 'description' : 'The requested item is already in the database'})

    new_item = Item(name=data['itemName'], amount=data['itemAmount'])

    db.session.add(new_item)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New item created', 'description' : 'An item has successfully been created'})

@app.route('/inventories/<itemNames>', methods=['DELETE'])
def delete_group_items():
    return ''

if __name__ == '__main__':
    app.run(debug=True)