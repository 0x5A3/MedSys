import platform
import database as DB
import webbrowser
import http.server
import HTML
import json
import store
import account

def page_login(arg):
    return HTML.page("MedSys Login", [
        HTML.card([
            HTML.title("MedSys"),
            HTML.subtitle("Sign in"),

            HTML.text_input("Enter your username",
                            div_id="username"),
            HTML.text_input("Enter your password",
                            div_id="password", in_type="password"),

            HTML.div([
                HTML.button("Next", onclick="login()"),
                HTML.button("Create Account",
                            onclick="goto('register')", style="text"),
            ])
        ], "card login")],

        scripts=["base.js", "login.js"],
        css=["style.css", "login.css"]
    )


def page_register(arg):
    return HTML.page("MedSys Register", [
        HTML.card([
            HTML.subtitle("MedSys"),
            HTML.title("Register"),

            HTML.text_input("Username", div_id="username"),
            HTML.text_input("First Name", div_id="name_first"),
            HTML.text_input("Last Name", div_id="name_last"),

            HTML.text_input("Email", div_id="email"),

            HTML.text_input("Password",
                            div_id="password", in_type="password"),
            HTML.text_input("Confirm Password",
                            div_id="password-confirm", in_type="password"),

            HTML.div([
                HTML.button("Create", onclick="register()"),
                HTML.button("Login", onclick="goto('login')", style="text"),
            ])
        ], "card login")],

        scripts=["base.js", "register.js"],
        css=["style.css", "login.css"]
    )



def page_error(code, msg):
    return HTML.page("MedSys Error", [
        HTML.card([
            HTML.title(f"Error {code}"),
            HTML.subtitle(msg)
        ])
    ], css=["style.css"])


def page_generic_error(arg):
    return page_error(500, "Internal server error")


page_maker = {
    "login": page_login,
    "register": page_register,

    "store": store.page_store,
    "checkout": store.page_checkout,
    "history": store.page_history,
    
    "account": account.page_profile,
    "error": page_generic_error,
}


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def respond(self, code, fmt, data=None):
        self.send_response(code)
        self.send_header("Content-type", fmt)
        self.end_headers()

        if data:
            self.wfile.write(data)

    def do_GET(self):
        path = "/login" if self.path == "/" else self.path

        path_parts = path[1:].split("/")
        domain, args = path_parts[0], path_parts[1:]

        if domain in page_maker:
            page = page_maker[domain](args).encode()
            self.respond(200, "text/html", page)
        else:
            self.respond(404, "text/html",
                         page_error(404, "File not found").encode())

    def json_apply(self, action):
        def apply(data):
            print("RECEIVED", data)
            data = json.dumps(action(json.loads(data))).encode()
            print("SENDING", data)
            self.respond(201, "application/json", data)
        return apply

    def do_POST(self):
        actions = {
            "/$login": self.json_apply(DB.login),
            "/$register": self.json_apply(DB.register),
            "/$search": self.json_apply(DB.search),

            "/$cart_add": self.json_apply(DB.cart_add),
            "/$cart_remove": self.json_apply(DB.cart_remove),
            "/$purchase": self.json_apply(DB.purchase),
        }

        data = self.rfile.read(int(self.headers["Content-Length"]))
        if self.path in actions:
            actions[self.path](data)
        else:
            self.respond(200, "text/html")

    def log_message(self, fmt, *args):
        msg, code, _ = args
        print(f"-- [{code}] {msg}")


def run_server(PORT=8040):
    with http.server.HTTPServer(("localhost", PORT), RequestHandler) as server:
        print(f"Starting server on {PORT}")

        if platform.system() == "Windows":
            path = f"http://localhost:{PORT}"
        else:
            path = f"localhost:{PORT}"

        webbrowser.open(path)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Quitting...")
