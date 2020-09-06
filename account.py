def page_profile(arg):
    if len(arg) != 1:
        results = [HTML.card(["Error 500: Internal Server Error"])]
        username = ""
    else:
        username = arg[0]
        
        if not results:
            results = [HTML.card(["No items found :("])]

    return HTML.page("Checkout", [
        HTML.node("script", f'let username = "{username}";'),
        HTML.node("div", [

            HTML.subtitle("Profile"),
            profile_icon(username),

            HTML.text_input("Billing Address", div_id="address"),
        ], {"id": "banner"}
        )] + results,
        scripts=["base.js", "store.js", "checkout.js"],
        css=["style.css", "store.css"]
    )
