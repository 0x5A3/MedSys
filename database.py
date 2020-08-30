import HTML
from mongo import MongoClient

client = MongoClient()

db = client.online_pharmacy

db_users = db.users
db_items = db.items
db_transactions = db.transactions

db_users.insert_one({
    "username": "a",
    "password": "a",
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



def Result(success, reason):
    return {"success": success, "reason": reason}
def Error(reason):
    return Result(False, reason)
def ServerError():
    return Error("Internal Server Error")
def Ok():
    return Result(True, "")


def register(state):
    user = db_users.find_one({"username": state["username"]})

    if user:
        return Error("user already exists")
    for field in ["username", "password", "email"]:
        if field not in state or not state[field]:
            return Error(f"{field} required")

    state["cart"] = {}
    db_users.insert_one(state)
    return Ok()


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

    def to_html(self, button, n, checkout, disabled = False):
        return HTML.div([
            HTML.div([self.name], {"class": "name"}),
            HTML.div([self.desc], {"class": "desc"}),

            HTML.div([
                HTML.span([f"{self.price} AED"]),
                HTML.leaf("input" + (" disabled" if disabled else ""), {
                    "type": "number", "class": "number",
                    "value": str(n), "min": "0", "max": str(self.stock),
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
        "stock": {"$gt": 0 }
    })

    user = db_users.find_one({ "username": username })
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
    user = db_users.find_one({ "username": username })

    if not user:
        return ServerError()

    price = 0

    cart, results = user["cart"], []
    for item_id in cart:
        item = db_items.find_one({ "item_id": int(item_id) })
        price += int(item["price"]) * int(cart[item_id])

        if not item:
            continue 

        results += [Item(item).checkout_remove(cart[item_id])]
    return results + [HTML.div(f"Price: {price} AED")]
    

def __cart_update(username, cart):
    db_users.update_one(
        { "username": username },
        { "$set": { "cart": cart } }
    )

def cart_add(state):
    try:
        username, item_id, n = state["username"], state["item_id"], state["quantity"]

        item = db_items.find_one({ "item_id": item_id })
        user = db_users.find_one({ "username": username })

        if not item or not username:
            return ServerError()

        cart = user["cart"]
        cart[str(item_id)] = int(n)
        __cart_update(username, cart)

        user = db_users.find_one({ "username": username })

        return Ok()
    except Exception as ex:
        print("#", ex)

    return ServerError()

def cart_remove(state):
    try:
        username, item_id = state["username"], state["item_id"]

        item = db_items.find_one({ "item_id": item_id })
        user = db_users.find_one({ "username": username })
        
        if not item or not user:
            return ServerError()

        cart = user["cart"]
        try:
            del cart[str(item_id)]
        except:
            pass
        
        __cart_update(username, cart)

        user = db_users.find_one({ "username": username })

        return Ok()
    except Exception as ex:
        print("#", ex)
    return ServerError()

def purchase(state):
    try:
        username = state["username"]
        user = db_users.find_one({ "username": username })

        print(user)
        if not user:
            return ServerError()

        cart = user["cart"]

        for item_id in cart:
            print(item_id, cart[item_id], type(cart[item_id]))
            item_verify = db_items.find_one({ 
                "item_id": int(item_id), 
                "stock": { "$gte": cart[item_id] }
            })
            print(item_verify)
            if not item_verify:
                return ServerError()

        for item_id in cart:
            db_items.update_one(
                { "item_id": int(item_id) },
                { "$inc": { "stock": -cart[item_id] }}
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