from pymongo import MongoClient

client = MongoClient()

db = client.online_pharmacy

db.users.drop()
db.items.drop()
db.transactions.drop()

users = db.users
users.insert_one({"Username": "johndoe69", "First Name": "John", "Last Name": "Doe",
                  "Password": "hellothere", "Email ID": "johndoe69@gmail.com",
                  "Billing Address": "Highway 37"})

items = db.items
items.insert_one({"item_id": 1, "Product Name": "Patanjali Hair Oil",
                  "Description": "Cures Cancer", "Price": 105, "Stock": 69})

transactions = db.transactions
transactions.insert_one({"transaction_id": 1, "Username": "johndoe69",
                         "Date": "05/07/2020", "Items Bought": [(1, 30)], "Total": 3150, "Shipped": True})


def get_item_info(item_id):
    desc_cursor = items.find({"item_id": item_id})
    for description in desc_cursor:
        return description


def name_checker(name, type_name):
    a = name.split()
    if len(a) != 1:
        return f"{type_name} Name should have only one word!"
    else:
        if name[0].isspace() or name[-1].isspace():
            return "Name cannot start or end with a whitespace!"
        elif name.isalpha():
            if name[0].isupper():
                if name[1:].islower():
                    return name
                else:
                    return "Only first letter should be capitalized!"
            else:
                return "First letter should be capitalized!"
        else:
            return "Name cannot contain characters other than the letters!"


def password_checker(password):
    upper_case = special_characters = numbers = 0
    if password[0].isspace() or password[-1].isspace():
        return "Password cannot start or end with a whitespace!"
    else:
        for character in password:
            if character.isalpha():
                if character.isupper():
                    upper_case += 1
                else:
                    pass
            elif character.isdigit():
                numbers += 1
            elif character.isspace():
                pass
            else:
                special_characters += 1
        length = len(password)

        error_list = []
        if length < 7:
            error_list.append("7 characters")
        if upper_case < 1:
            error_list.append("1 Upper Case")
        if numbers < 1:
            error_list.append("1 Number")
        if special_characters < 1:
            error_list.append("1 Special Character")

        error_length = len(error_list)
        if error_length == 0:
            return "Perfect Password!"
        else:
            error_message = "Password needs to have atleast "
            for i in range(error_length):
                if i != (error_length - 1):
                    error_message += f'{error_list[i]}, '
                elif i == 0:
                    error_message += f'{error_list[i]}!'
                else:
                    error_message += f'and {error_list[i]}!'
            return error_message


def register_account(username, first_name, last_name, password, email_id, billing_address):
    checker = users.find({"Username": username})
    if checker == []:
        users.insert_one({"Username": username, "First Name": first_name, "Last Name": last_name,
                          "Password": password, "Email ID": email_id, "Billing Address": billing_address})
        return "Registered!"
    else:
        return "Username already exists!"


def update_description(username, new_username=None, first_name=None, last_name=None, password=None, email_id=None, billing_address=None):
    a = ["Username", "First Name", "Last Name",
         "Password", "Email ID", "Billing Address"]
    b = [new_username, first_name, last_name,
         password, email_id, billing_address]
    update_query = "users.update_one({'Username': " + \
        f"'{username}'" + "}, {'$set': {"
    for i in range(6):
        if b[i] != None:
            update_query += f"'{a[i]}': '{b[i]}', "
        else:
            pass
    exec(update_query[:-2] + "}})")


def get_user_info(username):
    desc_cursor = users.find({"Username": username})
    for description in desc_cursor:
        return description


def get_transaction_info(transaction_id):
    desc_cursor = transactions.find({"transaction_id": transaction_id})
    for description in desc_cursor:
        return description


def user_transaction_info(username, latest=False):
    desc_cursor = transactions.find({"Username": username})
    if latest:
        return list(desc_cursor)[-1]
    else:
        return desc_cursor
