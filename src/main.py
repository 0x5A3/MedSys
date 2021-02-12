import database as DB
import server
import sys

if __name__ == "__main__":
    args = sys.argv    

    DB.start()
    if len(args) == 2 and args[1] == "reset":
        print("Resetting database ...")
        DB.reset()

    server.run_server()
    DB.quit()