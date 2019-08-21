from time import time


class ExpenseObject:
    def __init__(self, expense_item_name, payment_method, price, buyer):
        self.expense_item_name = expense_item_name
        self.payment_method = payment_method
        self.price = price
        self.buyer = buyer
        self.timestamp = int(time())

    def create_expense_dict(self):
        expense_dict = {
            "expense_item_name": self.expense_item_name,
            "payment_method" : self.payment_method,
            "price": self.price,
            "buyer": self.buyer,
            "timestamp": self.timestamp,
        }
        return expense_dict