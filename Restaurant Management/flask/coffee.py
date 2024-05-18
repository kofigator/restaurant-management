# coffee.py
from flask import Flask, render_template, request, redirect, url_for
import random
import string
from datetime import datetime

app = Flask(__name__)

def generate_random_order_number(initials, length):
    random_numbers = ''.join(random.choices(string.digits, k=length))
    return f"{initials}-{random_numbers}"

def calculate_total(order_list):
    total = 0
    for _, _, _, total_price in order_list:
        total += total_price
    return total

order_list = []  # Define order_list as an empty list


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/order', methods=['POST'])
# def order():
#     username = request.form['username']
#     choice = request.form['choice']
#     quantity = int(request.form['quantity'])

#     menu = {
#         "1": "Coffee",
#         "2": "Cappuccino",
#         "3": "Tea",
#         "4": "Hot Chocolate",
#         "5": "Tropical F.Juice",
#         "6": "Beef Roll",
#         "7": "Meat Pie",
#         "8": "Sandwich",
#         "9": "Cupcake",
#         "10": "Spring Roll",
#     }
#     item = menu[choice]
#     price = {
#         "Coffee": 30.00,
#         "Cappuccino": 50.00,
#         "Tea": 40.00,
#         "Hot Chocolate": 35.00,
#         "Tropical F.Juice": 60.00,
#         "Beef Roll": 20.00,
#         "Meat Pie": 10.00,
#         "Sandwich": 30.00,
#         "Cupcake": 25.00,
#         "Spring Roll": 15.00,
#     }[item]
#     total_price = price * quantity

#     if request.form['action'] == 'add_to_cart':
#         # Add the item to the cart list
#         order_list.append((item, quantity, price, total_price))
#         # Redirect back to the index page
#         return redirect(url_for('index'))

#     elif request.form['action'] == 'checkout':
#         # Handle checkout process
#         order_number = generate_random_order_number("Ord", 5)
#         total_price = calculate_total(order_list)
        
#         #to file
#         with open("C:/Users/user/Desktop/Py/area/order_summary.txt", "a") as to_File:
#             for item, quantity, unit_price, total_price in order_list:
#                 to_File.write(f"{username} {order_number} {item}, {quantity}, GHS {unit_price}, GHS {total_price} {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            
#         return render_template('order_summary.html', order_list=order_list, total_price=total_price, order_number=order_number, username=username)


@app.route('/')
def mainPage():
    return render_template('mainPage.html')
    

# @app.route('/staff_page')
# def staff_page():
#     return render_template('staff_page.html')

users = {
    "admin": "admin",
    "staff2": "password2",
    "staff3": "password3"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Valid login
            return redirect(url_for('staff_page'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/staff_page')
def staff_page():
    order_history = []
    with open("C:/Users/user/Desktop/repo/restaurant-management/Restaurant Management/flask/order_summary.txt", "r") as file:
        for line in file:
            order_history.append(line.strip().split(' '))
    return render_template('staff_page.html', order_history=order_history)




@app.route('/customer_page')
def customer_page():
    return render_template('customer_page.html')


@app.route('/order', methods=['POST'])
def order():
    username = request.form['username']
    choice = request.form['choice']
    quantity = int(request.form['quantity'])

    menu = {
        "1": "Coffee",
        "2": "Cappuccino",
        "3": "Tea",
        "4": "Hot Chocolate",
        "5": "Tropical F.Juice",
        "6": "Beef Roll",
        "7": "Meat Pie",
        "8": "Sandwich",
        "9": "Cupcake",
        "10": "Spring Roll",
    }
    item = menu[choice]
    price = {
        "Coffee": 30.00,
        "Cappuccino": 50.00,
        "Tea": 40.00,
        "Hot Chocolate": 35.00,
        "Tropical F.Juice": 60.00,
        "Beef Roll": 20.00,
        "Meat Pie": 10.00,
        "Sandwich": 30.00,
        "Cupcake": 25.00,
        "Spring Roll": 15.00,
    }[item]
    total_price = price * quantity

    if request.form['action'] == 'add_to_cart':
        # Add the item to the cart list
        order_list.append((item, quantity, price, total_price))
        # Redirect back to the index page
        return redirect(url_for('customer_page'))

    elif request.form['action'] == 'checkout':
        # Handle checkout process
        order_list.append((item, quantity, price, total_price))
        order_number = generate_random_order_number("Ord", 5)
        total_price = calculate_total(order_list)
        
        grand_total = 0  # Initialize the grand total

        # Loop through each order
        for item, quantity, unit_price, total_price in order_list:
            grand_total += total_price  # Accumulate the total price


        #to file
        with open("C:/Users/user/Desktop/repo/restaurant-management/Restaurant Management/flask/order_summary.txt", "a") as to_File:
            for item, quantity, unit_price, total_price in order_list:
                to_File.write(f"{username}, {order_number}, {item}, {quantity}, GHS {unit_price}, GHS {total_price}, {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            
        return render_template('order_summary.html', order_list=order_list, grand_total=grand_total, order_number=order_number, username=username)




    # Redirect or render appropriate page

if __name__ == "__main__":
    app.run(debug=True)
 