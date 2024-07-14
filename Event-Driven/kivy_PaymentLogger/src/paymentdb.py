## src/paymentdb.py
# @Import: paymentdb
# @Author: @Grimoors
# @Date: 2024-04-20
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-20 - 5:56 IST
# @Title: Payment Database
# @Description: A simple database to store payment details
## This file is used to create a database to store the payment details.
## The PaymentDB class is used to create a database and log the payment details to the database.
## The create_table method is used to create a table in the database to store the payment details.
## The log_payment method is used to log the payment details to the database.
## The close method is used to close the connection to the database.
## The PaymentDB class is used to create a database and log the payment details to the database.

import kivy_PaymentLogger.src.util.logger
logger = kivy_PaymentLogger.src.util.logger.Logger()

try:
    import sqlite3
except ImportError as e:
    # print('sqlite3 is not installed, please install sqlite3 first.')
    # print("Error Originated from file : paymentdb.py")
    # print('Error:', e)
    e_message = "sqlite3 is not installed, please install sqlite3 first." + "Error Originated from file : paymentdb.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

class PaymentDB:
    def __init__(self):
        self.conn = sqlite3.connect('./kivy_PaymentLogger/src/db/payments.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS payments
                            (id INTEGER PRIMARY KEY, p_type TEXT, label TEXT, amount REAL, 
                            t_date TEXT, t_id TEXT SECONDARY KEY, accnt_trace TEXT, merch_trace TEXT, category TEXT)''')
        self.conn.commit()

    def log_payment(self, p_type, label, amount, t_date, t_id, accnt_trace=None, merch_trace=None, category=None):
        self.cursor.execute('INSERT INTO payments (p_type, label, amount, t_date, t_id, accnt_trace, merch_trace, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                            (p_type, label, amount, t_date, t_id, accnt_trace, merch_trace, category))
        self.conn.commit()

    def close(self):
        self.conn.close()
