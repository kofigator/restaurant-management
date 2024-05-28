import sqlite3

connection = sqlite3.connect('Order.db', check_same_thread= False)
# we create a cursor object
cursor = connection.cursor()
# we create a table
cursor.execute(

    """CREATE TABLE Orders(
        OderID varchar(255) primary key,
        UserName Varchar(255),
        Item varchar(255), 
        Quantity Varchar(255),
        unitPrice flaot,
        TotalPrice float,
        log_date timestamp default current_timestamp

    );"""
)
# we commit our connection and close it
connection.commit()
cursor.close()
connection.close()