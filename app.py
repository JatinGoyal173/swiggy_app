from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, contact TEXT, 
                           restaurant TEXT, food_item TEXT, quantity INTEGER, total_price REAL)''')
        conn.commit()

init_db()

# Enhanced restaurant data with ratings
restaurants = {
    'Spicy Bites': {
        'description': "Authentic Indian flavors with a spicy twist!",
        'rating': 4.7,
        'menu': {'Biryani': 12, 'Noodles': 10, 'Paneer Tikka': 8}
    },
    'Pasta Palace': {
        'description': "Delicious Italian pasta dishes made with fresh ingredients.",
        'rating': 4.5,
        'menu': {'Pasta Alfredo': 15, 'Garlic Bread': 5, 'Lasagna': 18}
    },
    'Burger Hub': {
        'description': "Juicy burgers, crispy fries, and refreshing milkshakes!",
        'rating': 4.8,
        'menu': {'Cheeseburger': 8, 'Fries': 4, 'Milkshake': 6}
    },
    'Sushi World': {
        'description': "Experience the best sushi in town with fresh ingredients.",
        'rating': 4.6,
        'menu': {'Sushi Rolls': 20, 'Miso Soup': 8, 'Tempura': 12}
    },
    'Taco Fiesta': {
        'description': "Tacos, nachos, and burritos packed with bold flavors.",
        'rating': 4.4,
        'menu': {'Tacos': 10, 'Nachos': 7, 'Burrito': 12}
    },
    'Vegan Delights': {
        'description': "Healthy and delicious plant-based meals for every taste.",
        'rating': 4.9,
        'menu': {'Vegan Salad': 10, 'Tofu Stir Fry': 14, 'Smoothie': 7}
    },
    'Steakhouse Prime': {
        'description': "Premium cuts of steak grilled to perfection.",
        'rating': 4.7,
        'menu': {'Ribeye Steak': 25, 'Grilled Chicken': 18, 'Mashed Potatoes': 6}
    },
    'Seafood Haven': {
        'description': "Fresh seafood specialties prepared by top chefs.",
        'rating': 4.8,
        'menu': {'Grilled Salmon': 22, 'Lobster Bisque': 15, 'Shrimp Cocktail': 12}
    },
    'Pizza Paradise': {
        'description': "Stone-baked pizzas with fresh ingredients and a crispy crust.",
        'rating': 4.6,
        'menu': {'Margherita Pizza': 14, 'Pepperoni Pizza': 16, 'Veggie Pizza': 13}
    },
    'Dessert Delight': {
        'description': "Heavenly desserts and pastries for your sweet cravings.",
        'rating': 4.9,
        'menu': {'Chocolate Cake': 8, 'Cheesecake': 9, 'Ice Cream Sundae': 7}
    }
}

@app.route('/')
def home():
    return render_template('index.html', restaurants=restaurants)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        restaurant_name = request.form.get('restaurant')
        food_item = request.form.get('food')
        quantity = request.form.get('quantity')
        
        if not name or not contact or not restaurant_name or not food_item or not quantity:
            return "All fields are required!", 400
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return "Invalid quantity!", 400
        except ValueError:
            return "Quantity must be a number!", 400
        
        price_per_item = restaurants.get(restaurant_name, {}).get('menu', {}).get(food_item, 0)
        total_price = price_per_item * quantity
        
        return render_template('bill.html', name=name, contact=contact, 
                               restaurant=restaurant_name, food_item=food_item, 
                               quantity=quantity, price_per_item=price_per_item, 
                               total_price=total_price)
    
    return render_template('order.html', restaurants=restaurants)

@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form.get('name')
    contact = request.form.get('contact')
    restaurant_name = request.form.get('restaurant')
    food_item = request.form.get('food_item')
    quantity = int(request.form.get('quantity'))
    total_price = float(request.form.get('total_price'))

    with sqlite3.connect("order.html") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (name, contact, restaurant, food_item, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, contact, restaurant_name, food_item, quantity, total_price))
        conn.commit()

    return render_template('bill.html', name=name, contact=contact, 
                           restaurant=restaurant_name, food_item=food_item, 
                           quantity=quantity, total_price=total_price)

@app.route('/orders', methods=['GET'])
def get_orders():
    with sqlite3.connect("orders.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
