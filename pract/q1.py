# Q1 - Write a program to Insert a paragraph and 
# count the number of words in a text file “LINES.TXT”.

def get_para():
    print("Enter lines (Press Ctrl C/Ctrl D to complete)")
    
    lines = []
    while True:        
        try:
            lines += [input("> ")]
        except KeyboardInterrupt:
            print()
            break
    return '\n'.join(lines)

def count(path):
    with open(path, "r") as file:
        count = 0
        for line in file:
            count += len(line.split())
    return count

print("File program")
path = input("Enter file path: ")

with open(path, "w") as file:
    file.write(get_para())
print("No of words: ", count(path))