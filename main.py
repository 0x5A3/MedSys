import database as DB
import server

if __name__ == "__main__":
    DB.start()
    server.run_server()
    DB.quit()