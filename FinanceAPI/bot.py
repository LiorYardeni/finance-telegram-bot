import logging
from os import environ
from time import sleep

from expenses_object import ExpenseObject
from categories_object import CategoriesObject
from configuration import get_config
# from mapping import classify


from pymongo import MongoClient
import telegram
from telegram.error import NetworkError, Unauthorized

DB_FINANCE = get_config('db_finance')
DB_EXPENSES_NAME = get_config('db_expenses_name')
DB_CATEGORIES_NAME = get_config('db_categories_name')


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


client = MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_FINANCE}')
db = client['finance']


update_id = 0

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('finance.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(get_config('token'))

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None


    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1
            break


def value_count(text_content):
    # check how many values are divided by ","
    value_counter = 1
    for character in text_content:
        if character == ",":
            value_counter += 1
    return value_counter


def reply_message_invalid(update):
    update.message.reply_text(
        "The last message you entered is not in the correct format,"
        " please follow the pattern \n\"payment method, item, price\"")


def get_text_content(update):
    #get  3 values messages only from group chat,
    text_content = update.message['text']
    # buyer = update.message.chat["first_name"] #for private chat, not group
    buyer = update.message['from_user']['first_name']
    if value_count(text_content) == 3:
        return text_content, buyer
    else:
        return None, None
    # else:
    #     reply_message_invalid(update)


def create_expense_dict(text_content, buyer):
    payment_method, expense_item_name, price = map(lambda x: x.strip(), text_content.split(","))
    price = int(price)
    # TO DO Case sensitivity
    #TO DO plural

    expense_obj = ExpenseObject(expense_item_name=expense_item_name,
                                payment_method=payment_method,
                                price=price,
                                buyer=buyer,)
    expense_dict = expense_obj.create_expense_dict()
    return expense_dict

#
# def check_category(expense_item_name):
#     category =
#     for k,v in categories_dict:
#         if k == expense_item_name:
#             return category_name
#         else:
#             return category = unsorted


def create_categories_dict(expense_item_name, category_name):
    category_obj = CategoriesObject(category_name=category_name, expense_item_name=expense_item_name)
    category_dict = category_obj.create_categories_dict()
    return category_dict


def insert_to_expenses_db(expense_dict):
    expenses_collection = db.expenses
    expense_id = expenses_collection.insert_one(expense_dict).inserted_id
    return expense_id

# def create_categories_dict(expense_item_name):


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            text_content, buyer = get_text_content(update)
            if not text_content or not buyer:
                reply_message_invalid(update)

            else:
                logger.info('test')
                message = f'A message was received with the following content: {text_content}'
                logger.info(message)
                expenses_dict = create_expense_dict(text_content, buyer)
                insert_to_expenses_db(expenses_dict)


if __name__ == '__main__':
    main()