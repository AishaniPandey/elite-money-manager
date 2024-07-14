from abc import ABC, abstractmethod
from util.json_File_Handler import json_File_Handler

# Define the Strategy interface
class CheckTransactionExistsStrategy(ABC):
    @abstractmethod
    def exists(self, t_id):
        pass

# Concrete strategy for SQLite
class SQLiteCheckTransactionExists(CheckTransactionExistsStrategy):
    def __init__(self, db_path):
        self.db_path = db_path

    def exists(self, t_id):
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT EXISTS(SELECT 1 FROM payments WHERE t_id = ? LIMIT 1)", (t_id,))
            exists = cursor.fetchone()[0]
        return exists

# Concrete strategy for JSON
class JSONCheckTransactionExists(CheckTransactionExistsStrategy):
    def __init__(self, json_path):
        self.json_path = json_path
        self.handler = json_File_Handler()

    def exists(self, t_id):
        return self.handler.search_Transaction_By_t_id(self.json_path, t_id)

# # Usage in your application
# class PaymentLogger:
#     def __init__(self, db_checker, json_checker):
#         self.db_checker = db_checker
#         self.json_checker = json_checker

#     def log_payment(self, t_id, **kwargs):
#         if self.db_checker.exists(t_id) or self.json_checker.exists(t_id):
#             toast("Transaction with this ID has already been logged.")
#             return
#         # Log payment since no duplicates were found
#         # Continue with the logging process...
