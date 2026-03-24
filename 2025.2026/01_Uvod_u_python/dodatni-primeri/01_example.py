
import sys
import os


# print(len(args))
# print(args)

# a = input("Please enter a number: ")
# print(int(a))

# with open("text.txt", "r") as f:
#     print(f.read())

# os.listdir(dir)

# python3 cat input.txt 
# python3 cp input.txt output.txt
# python3 ls path

# map = {key:value,....}
# numbers = {"one":1, "two": 2, "three": 3}...
# numbers["one"] -> 1

def saberi(a:int, b:int) -> int:
    return a + b

def cat(args):
    if len(args) != 3:
        print("Usage: python3 01_example.py cat path")
        sys.exit(1)
    with open(args[2]) as f:
        print(f.read())

def cp(args):
    if len(args) != 4:
        print("Usage: python3 01_example.py cp input output")
        sys.exit(1) 
    with open(args[2], "r") as f_input:
        with open(args[3], "w") as f_output:
            f_output.write(f_input.read())

def ls(args):
    if len(args) != 3:
        print("Usage: python3 01_example.py ls dir")
        sys.exit(1)
    entries = os.listdir(args[2])
    for e in entries:
        print(e)

commands = {
    "cp": cp,
    "cat": cat,
    "ls": ls
}

try:
    cmd = commands[sys.argv[1]]
    cmd(sys.argv)
except:
    print("No such command: ", sys.argv[1])
