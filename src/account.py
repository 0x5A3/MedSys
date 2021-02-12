from store import *
from server import *

def page_profile(arg):
    if len(arg) != 1:
        return page_generic_error(arg)    
    
    username = arg[0]
    user = DB.get_user(username)
    

    return HTML.page("Profile", [
        HTML.node("script", f'let username = "{username}";'),
        HTML.node("div", [
            
            HTML.card(
                [
                    HTML.subtitle("Profile"),
                    profile_icon(username),

                    f"""
                        First name: {user['name_first']}
                        <br> Last name: {user['name_last']}

                        <br>
                        <br> Username: {user['username']}
                        <br> Email: {user['email']}
                    """,
                    HTML.div(
                        [
                            HTML.button("Back", onclick="goto_store()"),
                            HTML.button("Log out", onclick="exit()")
                        ]
                    )
                ],

            )
        ], {"id": "banner"}
        )],
        scripts=["base.js", "store.js", "account.js"],
        css=["style.css", "login.css"]
    )
