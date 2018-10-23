from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ingredients = db.relationship('Ingredient', backref='ingredients', lazy=True)

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
