#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return [restaurant.to_dict() for restaurant in restaurants], 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        return restaurant.to_dict(include_pizzas=True), 200
    else:
        return {"error": "Restaurant not found"}, 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        # Delete associated restaurant_pizzas first
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return {"error": "Restaurant not found"}, 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in pizzas], 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['price', 'pizza_id', 'restaurant_id']):
            return {"errors": ["validation errors"]}, 400
        
        # Create new restaurant_pizza
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        # Return the restaurant_pizza data with all expected fields
        return restaurant_pizza.to_dict(), 201
        
    except ValueError as e:
        return {"errors": [str(e)]}, 400
    except Exception as e:
        # Handle other exceptions like foreign key constraints
        return {"errors": ["validation errors"]}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)