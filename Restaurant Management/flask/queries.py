from flask import g
import sqlite3
from datetime import datetime, timedelta, date

DATABASE = 'Order.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, check_same_thread=False)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def addorder(orderID, username, item, quantity, unitPrice, totalPrice):
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Orders(OrderID, Username, Item, Quantity, UnitPrice, TotalPrice, LogDate)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (orderID, username, item, quantity, unitPrice, totalPrice, datetime.now().strftime('%Y-%m-%d'))
        )
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

def display_order():
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM Orders;""")
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        result = []
    finally:
        cursor.close()
    return result

def displayToday_Order():
    today = date.today().strftime('%Y-%m-%d')
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM Orders WHERE DATE(LogDate) = ?;""", (today,))
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        result = []
    finally:
        cursor.close()
    return result

def yesterday_Order():
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM Orders WHERE DATE(LogDate) = ?;""", (yesterday,))
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        result = []
    finally:
        cursor.close()
    return result

def date_Order(Date):
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT * FROM Orders WHERE DATE(LogDate) = ?;""", (Date,))
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        result = []
    finally:
        cursor.close()
    return result
