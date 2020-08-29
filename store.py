import HTML
import database as DB


def page_store(arg):
    if len(arg) != 2:
        results = [HTML.card(["Error 500: Internal Server Error"])]
        username, query = "", ""
    else:
        username, query = arg
        results = DB.search(username, query)    

        if not results:
            results = [HTML.card(["No items found :("])]

    return HTML.page("Store", [
        HTML.node("script", f'let username = "{username}";'),
        HTML.node("div", [
            HTML.subtitle("MedSys Store"),
            HTML.text_input("Search",
                            div_id="search",
                            onkeydown="search(this)",
                            value=query),
            HTML.button("Go to checkout", onclick=f"goto_checkout()")
        ], {"id": "banner"}
        )] + results,
        scripts=["base.js", "store.js"],
        css=["style.css", "store.css"]
    )


def page_checkout(arg):
    if len(arg) != 1:
        results = [HTML.card(["Error 500: Internal Server Error"])]
        username, query = "", ""
    else:
        username = arg[0]
        results = DB.checkout(username)
        
        if not results:
            results = [HTML.card(["Empty Cart :P"])]

    return HTML.page("Checkout", [
        HTML.node("script", f'let username = "{username}";'),
        HTML.node("div", [

            HTML.subtitle("Checkout"),

            HTML.text_input("Billing Address", div_id="address"),
            HTML.button("Purchase", onclick=f"purchase()"),
            HTML.button("Store", onclick=f"goto_store()"),
        ], {"id": "banner"}
        )] + results,
        scripts=["base.js", "store.js", "checkout.js"],
        css=["style.css", "store.css"]
    )
