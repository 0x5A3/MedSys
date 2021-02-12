import mysql.connector as sql_connect

db = sql_connect.connect(
    host="localhost",
    user="guest",
    passwd="tiger"
)

cur = db.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS school;")
cur.execute("USE school;")
cur.execute("""CREATE TABLE IF NOT EXISTS school
(
    RollNo INT(5) PRIMARY KEY,
    Name VARCHAR(30),
    Class VARCHAR(5),
    Gender CHAR(4) CHECK (Gender IN ('F', 'M', 'O')),
    City VARCHAR(30),
    Marks INT(4)
)""")

cur.execute("SELECT MAX(RollNo) FROM school")
print(cur.fetchall())


def get_roll():
    try:
        roll = int(input("Roll no: "))
        if roll < 1:
            raise ValueError
        return roll
    except:
        print("Error: Expected number in {1,2,...} ")
        raise ValueError

def get_gender():
    gen = input("Gender: ")
    if gen in "FMO":
        return gen
    print("Error: Expected F, M or O")
    raise ValueError

def get_marks():
    try:
        marks = float(input("Marks: "))
        if not (0 <= marks <= 600):
            raise ValueError
        return marks
    except:
        print("Error: Expected decimal in [0.0-600.0]")
        raise ValueError


def view():
    cur.execute("SELECT * FROM school")
    for row in cur.fetchall():
        print(' | '.join(map(str, row)))

def add():
    try:
        print("New record")
        cur.execute(f"""
            INSERT INTO school 
                VALUES (
                    {get_roll()},
                    "{input("Name: ")}", 
                    "{input("Class: ")}", 
                    "{get_gender()}", 
                    "{input("City: ")}", 
                    {get_marks()}
                );
        """)
    except ValueError:
        pass

def rem():
    roll = get_roll()
    
    cur.execute(f"""
        SELECT Name 
            FROM school 
            WHERE RollNo = {roll}
    """)

    matches = cur.fetchall()
    if len(matches) == 0:
        print("No matches found")
    elif len(matches) == 1:
        print("Confirm deletion of")
        print(f"Roll no: {roll}")
        print(f"Name: {matches[0][0]}")

        if input(f"(y/n):") == "y":
            cur.execute(f"""
                DELETE 
                    FROM school 
                    WHERE RollNo = {roll};
            """)
            print(f"Roll no. {roll} Deleted")
        else:
            print("Operation cancelled")

def mod():
    roll = get_roll()

    cmd = f"""
        UPDATE school
            SET 
                Name = "{input("Name: ")}", 
                Class = "{input("Class: ")}", 
                Gender = "{get_gender()}", 
                City = "{input("City: ")}", 
                Marks = {get_marks()}
            WHERE
                RollNo = {roll};
    """

    if input("Confirm modification (y/n) ?: ") == "y":
        cur.execute(cmd)
        print(f": Roll no. {roll} Modified")
    else:
        print(": Operation Cancelled")

def prog_help():
    for name, (_, msg) in cmds.items():
        print(f"{name}: {msg}")


cmds = {
    "help": (prog_help, "display this message"),
    "add": (add, "add record"),
    "rem": (rem, "remove record"),
    "mod": (mod, "modify record"),
    "view": (view, "view records"),
    "quit": (quit, "quit program")
}



print("School Database")
print("type help to get help")

while True:
    cmd = input("> ").strip().lower()
    if cmd in cmds:
        fn, _ = cmds[cmd]
        fn()
    else:
        print(f"{cmd} is not defined")