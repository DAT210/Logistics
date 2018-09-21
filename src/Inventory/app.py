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

@app.route('/inventory', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    output = []

    for item in items:
        item_data = {}
        item_data['name'] = item.name
        item_data['amount'] = item.amount
        output.append(item_data)

    return jsonify({'items' : output})

@app.route('/inventory/<item_names>', methods=['GET'])
def get_group_items():
    return ''

@app.route('/inventory/<item_name>/<item_amount>', methods=['PUT'])
def update_item_amount():
    return ''

@app.route('/inventory', methods=['POST'])
def create_new_item():
    data = request.get_json()
    test = Item.query.filter_by(name=data['item_name']).first()
    if test:
        return jsonify({'code' : '1234', 'message' : 'New item not created', 'description' : 'The requested item is already in the database'})

    new_item = Item(name=data['item_name'], amount=data['item_amount'])

    db.session.add(new_item)
    db.session.commit()
    return jsonify({'code' : '201', 'message' : 'New item created', 'description' : 'An item has successfully been created'})

@app.route('/inventory/<item_names>', methods=['DELETE'])
def delete_group_items():
    return ''

if __name__ == '__main__':
    app.run(debug=True)