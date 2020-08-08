import http.server

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def respond(self, data, code = 200, fmt = "text/html"):
        self.send_response(code)
        self.send_header("Content-type", fmt)
        self.end_headers()

        if data:
            self.wfile.write(data)

    def respond_err(self, msg, code):
        with open("error.html") as file:
            self.respond(
                file.read()
                    .replace("{code}", str(code))
                    .replace("{message}", msg)
                    .encode())
    
    def do_GET(self):
        #Send data to client

        if self.path == "/":
            path = "index.html"
        else:
            path = self.path[1:]

        try:
            with open(path) as file:
                data = file.read()
            self.respond(data.encode())
        except FileNotFoundError:
            self.respond_err("File not found", 404)
        except Exception as ex:
            self.respond_err("Internal Server Error", 500)
            print("-- Exception!: {ex}")

    def do_POST(self):
        #Recieve data from client

        print(self.rfile.read(self.self.headers["Content-Length"]))
        self.repond("Success!")

    def log_message(self, format, *args):
        print(f"-- [{args[1]}] : {args[0]}")


def run_server(PORT = 8000):
    #Set up http daemon at given port and open default webbrowser at site

    with http.server.HTTPServer(("localhost", PORT), RequestHandler) as httpd:
        try:
            webpage_address = f"localhost:{PORT}"
            webbrowser.open(webpage_address)

            print("Starting server!")
            print(f"-- Serving on PORT {PORT}, at '{webpage_address}'")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Quitting server...")

import webbrowser
import sys       

if __name__ == "__main__":
    # Use sys.argv to get commandline arguments
    # eg: python3 main.py 8000 => sys.argv = ('main.py', '8000')

    if len(sys.argv) == 2:
        try:
            PORT = int(sys.argv[1])

            if PORT < 0:
                print(f"Error: PORT= {PORT}, must be a postive integer")
            else:
                run_server(PORT)
        except Exception as ex:
            print(f"Unexpected Internal Error!: \n-- {str(ex)}")
    elif(len(sys.argv)) == 1:
        run_server(8000)  
    else:
        print(f"Invalid arguments!")
    