from flask import Flask, render_template, request, redirect, url_for, session
import queries   # type: ignore
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

def generate_random_order_number():
    orderdate = datetime.now()
    anydate = datetime.strftime(orderdate, '%d%M%S')
    return anydate

def calculate_total(order_list):
    total = 0
    for _, _, _, total_price in order_list:
        total += total_price
    return total

@app.route('/home')
def mainPage():
    return render_template('mainPage.html')

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
            return redirect(url_for('staff_page'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/staff_page', methods=['POST', 'GET'])
def staff_page():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "all_orders":
            result = queries.display_order()
            return render_template('staff_page.html', message=result)
        elif action == "today_orders":
            result = queries.displayToday_Order()
            return render_template('staff_page.html', message=result)
        elif action == "yesterday_orders":
            result = queries.yesterday_Order()
            return render_template('staff_page.html', message=result)
        elif 'Date' in request.form:
            date_input = request.form.get('Date')
            if date_input:  # Check if date input is provided
                try:
                    date = datetime.strptime(date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
                    result = queries.date_Order(date)
                    return render_template('staff_page.html', message=result)
                except ValueError:
                    return render_template('staff_page.html', message="Invalid date format. Please use YYYY-MM-DD.")
            else:
                return render_template('staff_page.html', message="Please provide a date.")
    return render_template('staff_page.html')

@app.route('/customer_page', methods=['GET', 'POST'])
def customer_page():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add_to_cart':
            session['username'] = request.form['username']
        return redirect(url_for('order'))
    return render_template('customer_page.html', username=session.get('username'))

@app.route('/order', methods=['POST'])
def order():
    username = session.get('username')
    if not username:
        username = request.form['username']
        session['username'] = username

    choice = request.form.get('choice')
    quantity = int(request.form['quantity'])

    menu = {
        "1": "Coffee",
        "2": "Cappuccino",
        "3": "Tea",
        "4": "Hot-Chocolate",
        "5": "Tropical-F.Juice",
        "6": "Beef-Roll",
        "7": "Meat-Pie",
        "8": "Sandwich",
        "9": "Cupcake",
        "10": "Spring-Roll",
    }
    item = menu[choice]
    price = {
        "Coffee": 30.00,
        "Cappuccino": 50.00,
        "Tea": 40.00,
        "Hot-Chocolate": 35.00,
        "Tropical-F.Juice": 60.00,
        "Beef-Roll": 20.00,
        "Meat-Pie": 10.00,
        "Sandwich": 30.00,
        "Cupcake": 25.00,
        "Spring-Roll": 15.00, 
    }[item]
    total_price = price * quantity

    order_list = session.get('order_list', [])
    order_list.append((item, quantity, price, total_price))
    session['order_list'] = order_list  # Update session with the new order list

    if request.form['action'] == 'add_to_cart':
        return redirect(url_for('customer_page'))

    elif request.form['action'] == 'checkout':
        order_number = generate_random_order_number()
        grand_total = calculate_total(order_list)

        for item, quantity, unit_price, total_price in order_list:
            queries.addorder(order_number, username, item, quantity, unit_price, total_price)
        
        order_summary = {
            'order_list': order_list,
            'grand_total': grand_total,
            'order_number': order_number,
            'username': username
        }

        session.pop('order_list', None)  # Clear the order list from session after checkout
        session.pop('username', None)  # Clear the session after checkout
        return render_template('order_summary.html', **order_summary)

    return redirect(url_for('customer_page'))

if __name__ == "__main__":
    app.run(debug=True)
