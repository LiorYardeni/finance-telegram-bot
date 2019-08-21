class CategoriesObject:
    def __init__(self, expense_item_name, category_name):
        self.expense_item_name = expense_item_name
        self.category_name = category_name

    def create_categories_dict(self):
        categories_dict = {
            "category_name": self.category_name,
            "expense_item_name": self.expense_item_name,
        }
        return categories_dict