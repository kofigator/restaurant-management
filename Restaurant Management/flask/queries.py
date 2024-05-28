
from flask import g
import sqlite3
from datetime import datetime, timedelta
from datetime import date
def addorder(orderID, username, item, Quqntity, unitPrice, TotalPrice):

    connection = sqlite3.connect('Order.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO Orders(OderID, UserName, Item, Quantity, unitPrice, TotalPrice)
        VALUES('{orderID}', '{username}', '{item}', '{Quqntity}', '{unitPrice}', '{TotalPrice}');""".format(orderID=orderID, username=username, item=item, Quqntity=Quqntity, unitPrice=unitPrice, TotalPrice= TotalPrice)

    )
    connection.commit()
    cursor.close()
    connection.close()


def display_order():
    connection = sqlite3.connect('Order.db', check_same_thread=False)
    # connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM Orders;"""

    )
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result
def displayToday_Order():
    today = date.today()
    connection = sqlite3.connect('Order.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM Orders where DATE(log_date) = '{today}';""".format(today = today)

    )
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result
def yesterday_Order():
    yesterday = (datetime.now()-timedelta(1)).strftime('%Y-%m-%d')
    connection = sqlite3.connect('Order.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM Orders where DATE(log_date) = '{yesterday}';""".format(yesterday = yesterday)

    )
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result

def date_Order(Date):
    connection = sqlite3.connect('Order.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """SELECT * FROM Orders where DATE(log_date) = '{Date}';""".format(Date = Date)

    )
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result
    
