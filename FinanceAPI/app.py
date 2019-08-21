from configuration import get_config

from os import environ

from flask import Flask, request
from pymongo import MongoClient

DB_FINANCE = get_config('db_finance')

app = Flask(__name__)

if 'DYNO' in environ:
    DB_USERNAME = environ['DB_USERNAME']
    DB_PASSWORD = environ['DB_PASSWORD']
    DB_PORT = environ['DB_PORT']
    DB_URL = environ['DB_URL']

else:
    DB_USERNAME = get_config('db_username')
    DB_PASSWORD = get_config('db_password')
    DB_URL = get_config('db_url')
    DB_PORT = get_config('db_port')

client = MongoClient(f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_FINANCE}")
db = client['finance']
categories_collection = db.categories


@app.route('/insert_expense_item_name', methods=['POST'])
def insert_expense_item_name():
    content = request.json
    if not get_category_for_expense_item_name(content['expense_item_name']):
        id = categories_collection.insert_one(content)
        if id:
            return "ok"
    else:
        return "item already exists"


@app.route('/get_category_for_expense_item_name/<expense_item_name>', methods=['GET'])
def get_category_for_expense_item_name(expense_item_name):
    myquery = {"expense_item_name": expense_item_name}
    category_obj = categories_collection.find(myquery)
    if category_obj.count() >= 1:
        for x in category_obj:
            category_name = x['category_name']
            return category_name
    else:
        return None


if __name__ == '__main__':
    port = int(environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', use_reloader=True, port=port)