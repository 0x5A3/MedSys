# Write a menu driven program to implement the 
# STACK operations PUSH, POP and VIEW.

STACK = []

def push():
    STACK.append(input("elem: "))
    
def pop():
    if len(STACK) > 0:
        STACK.pop()
    else:
        print("stack underflow!")

def view():
    print(STACK)

def prog_help():
    for name, (_, msg) in cmds.items():
        print(f"{name}: {msg}")

cmds = {
    "help": (prog_help, "display this message"),
    "push": (push, "push element on top of stack"),
    "pop": (pop, "pop element from top of stack"),
    "view": (view, "view stack"),
    "quit": (quit, "exit program")
}

print("Stack program")
print("type help to get help")

while True:
    cmd = input("> ").strip().lower()
    if cmd in cmds:
        fn, _ = cmds[cmd]
        fn()
    else:
        print(f"{cmd} is not defined")