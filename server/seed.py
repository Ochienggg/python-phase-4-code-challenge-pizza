from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Clear existing data
    RestaurantPizza.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
    
    # Create restaurants
    restaurants = [
        Restaurant(name="Karen's Pizza Shack", address="address1"),
        Restaurant(name="Sanjay's Pizza", address="address2"),
        Restaurant(name="Kiki's Pizza", address="address3")
    ]
    
    # Create pizzas
    pizzas = [
        Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese"),
        Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"),
        Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    ]
    
    # Create restaurant pizzas
    restaurant_pizzas = [
        RestaurantPizza(price=1, pizza_id=1, restaurant_id=1),
        RestaurantPizza(price=5, pizza_id=1, restaurant_id=3),
        RestaurantPizza(price=10, pizza_id=2, restaurant_id=2),
        RestaurantPizza(price=15, pizza_id=3, restaurant_id=1),
        RestaurantPizza(price=20, pizza_id=3, restaurant_id=3)
    ]
    
    # Add to session and commit
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    
    print("Database seeded successfully!")