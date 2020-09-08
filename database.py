import HTML
from pymongo import MongoClient


def start():
    global db
    global db_users
    global db_items
    global db_transactions

    client = MongoClient()

    db = client.online_pharmacy
    db_users = db.users
    db_items = db.items
    db_transactions = db.transactions

    db_users.insert_one({
        "username": "a",
        "password": "a",
        "name_first": "Alex",
        "name_first": "Anderson",
        "email": "root@gmail.com",
        "cart": {}
    })
    db_items.insert_one({
        "item_id": 32,
        "name": "Patanjali hair OILE",
        "desc": "Cures Cancer",
        "price": 105,
        "stock": 69
    })
    db_items.insert_one({
        "item_id": 512000132,
        "name": "Ibuprofen",
        "desc": "RS-2-(4-(2-methylpropyl)phenyl)propanoic acid",
        "price": 20,
        "stock": 30
    })


def quit():
    pymongo.quit()


def Result(success, reason):
    return {"success": success, "reason": reason}


def Error(reason):
    return Result(False, reason)


def ServerError():
    return Error("Internal Server Error")


def Ok():
    return Result(True, "success")


def username_checker(username, field_name):
    if len(username) > 15:
        return f"{field_name} cannot be more than 15 characters!"

    if username[0].isdigit():
        return f"{field_name} should start with a letter or an underscore"
    # no capital letters
    for i in username:
        if i.isalpha:
            return None
    else:
        return f"{field_name} should contain atleast 1 letter!"


def name_checker(name, field_name):
    if len(name) > 15:
        return f"{field_name}: cannot be more than 10 characters!"

    if name[0].isupper():
        if len(name) == 1 or name[1:].islower():
            msg = None
        else:
            msg = f"{field_name}: Only first letter should be capitalized!"
    else:
        msg = f"{field_name}: First letter should be capitalized!"

    return msg

def email_checker(email, field_name):
    if email[0].isalpha() == False:
        return f"{field_name} should start with a letter!"

    if email.count("@") != 1:
        return f"{field_name} should contain exactly one '@'!"

    for i in '.@':
        index = 0
        old_index = None
        while old_index != index:
            old_index = index
            index = old_index + email[old_index:].find(i)
            #print(old_index, index)
            try:
                if email[index + 1] in '.@':
                    return f"{field_name} cannot use special characters next to each other!"

            except:
                return f"Cannot end {field_name} with '.' or '@'!"

    second_part = email.split('@')[-1]
    if second_part.count('.') != 1:
        return f"Enter valid domain in {field_name}!"

def password_checker(password, field_name):
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
            return None
        else:
            error_message = f"{field_name} needs to have atleast "
            for i in range(error_length):
                if i != (error_length - 1):
                    error_message += f'{error_list[i]}, '
                elif i == 0:
                    error_message += f'{error_list[i]}!'
                else:
                    error_message += f'and {error_list[i]}!'
            return error_message


def register(state):
    user = db_users.find_one({"username": state["username"]})

    def FieldError(msg, div_id):
        return {
            "success": False,
            "reason": msg,
            "div_id": div_id
        }

    if user:
        return FieldError("user already exists", "username")

    field_names = {
        "username": ("Username", username_checker),

        "name_first": ("First name", name_checker),
        "name_last": ("Last name", name_checker),

        "email": ("Email", email_checker),

        "password": ("Password", password_checker),
    }
    for field_key in field_names:
        field_name, field_checker = field_names[field_key]

        if field_key not in state or not state[field_key]:
            return FieldError(f"{field_name} required", field_key)

        msg = field_checker(state[field_key], field_name)
        if msg is not None:
            return FieldError(msg, field_key)

    state["cart"] = {}
    db_users.insert_one(state)
    return Ok()


def get_names(username):
    user = db_users.find_one({"username": username})
    return user["name_first"], user["name_last"]


def login(state):
    if db_users.find_one(state):
        return Ok()
    return Error("incorrect username/password")

class Item:
    Attr_Map = [
        "item_id",
        "name",
        "desc",
        "price",
        "stock"
    ]

    def __init__(self, attr_dict):
        for attr in Item.Attr_Map:
            if attr in attr_dict:
                setattr(self, attr, attr_dict[attr])
            else:
                raise Exception(f"Attribute missing {attr}")

    def to_html(self, button, n, checkout, disabled=False):
        return HTML.div([
            HTML.div([self.name], {"class": "name"}),
            HTML.div([self.desc], {"class": "desc"}),

            HTML.div([
                HTML.span([f"{self.price} AED"]),
                HTML.leaf("input" + (" disabled" if disabled else ""), {
                    "type": "number", "class": "number",
                    "value": str(n), "min": "1", "max": str(self.stock),
                    "oninput": f"add_item_quantity(this, {self.item_id}, {checkout})"
                }), button],
                {"class": "select"}
            )],

            {"id": f"item-{self.item_id}", "class": "item"}
        )

    def cart_add(self):
        return self.to_html(
            HTML.button("Add to cart", f"add_item(this, {self.item_id})"), 0, "false", True)

    def cart_remove(self, n):
        return self.to_html(
            HTML.button("Remove", f"remove_item(this, {self.item_id})"), n, "false")

    def checkout_remove(self, n):
        return self.to_html(
            HTML.button("Remove", f"checkout_remove(this, {self.item_id})"), n, "true")

def search(username, query):
    query = " ".join(query.split())  # remove redundant spaces

    matches = db_items.find({
        "name": {"$regex": query, "$options": "i"},
        "stock": {"$gt": 0}
    })

    user = db_users.find_one({"username": username})
    if not user:
        return []

    cart = user["cart"]

    results = []
    for item in matches:
        item = Item(item)
        __id = str(item.item_id)

        if __id in cart:
            results += [item.cart_remove(cart[__id])]
        else:
            results += [item.cart_add()]
    return results

def checkout(username):
    user = db_users.find_one({"username": username})

    if not user:
        return ServerError()

    price = 0

    cart, results = user["cart"], []
    for item_id in cart:
        item = db_items.find_one({"item_id": int(item_id)})
        price += int(item["price"]) * int(cart[item_id])

        if not item:
            continue

        results += [Item(item).checkout_remove(cart[item_id])]
    return results + [HTML.div(f"Price: {price} AED")]


def __cart_update(username, cart):
    db_users.update_one(
        {"username": username},
        {"$set": {"cart": cart}}
    )

def cart_add(state):
    try:
        username, item_id, n = state["username"], state["item_id"], state["quantity"]

        item = db_items.find_one({"item_id": item_id})
        user = db_users.find_one({"username": username})

        if not item or not username:
            return ServerError()

        cart = user["cart"]
        cart[str(item_id)] = int(n)
        __cart_update(username, cart)

        user = db_users.find_one({"username": username})

        return Ok()
    except Exception as ex:
        print("#", ex)

    return ServerError()

def cart_remove(state):
    try:
        username, item_id = state["username"], state["item_id"]

        item = db_items.find_one({"item_id": item_id})
        user = db_users.find_one({"username": username})

        if not item or not user:
            return ServerError()

        cart = user["cart"]
        try:
            del cart[str(item_id)]
        except:
            pass

        __cart_update(username, cart)

        user = db_users.find_one({"username": username})

        return Ok()
    except Exception as ex:
        print("#", ex)
    return ServerError()

def purchase(state):
    try:
        username = state["username"]
        user = db_users.find_one({"username": username})

        print(user)
        if not user:
            return ServerError()

        cart = user["cart"]

        for item_id in cart:
            print(item_id, cart[item_id], type(cart[item_id]))
            item_verify = db_items.find_one({
                "item_id": int(item_id),
                "stock": {"$gte": cart[item_id]}
            })
            print(item_verify)
            if not item_verify:
                return ServerError()

        for item_id in cart:
            db_items.update_one(
                {"item_id": int(item_id)},
                {"$inc": {"stock": -cart[item_id]}}
            )

        import datetime
        transaction = {
            "username": username,
            "address": state["address"],
            "info": cart,
            "time": str(datetime.datetime.now())
        }
        db_transactions.insert_one(transaction)

        __cart_update(username, {})

        return Ok()
    except Exception as ex:
        print("#", ex)
    return ServerError()
