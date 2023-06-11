from sys import argv

assert len(argv) == 2

with open(argv[1], "a") as file:
    file.write("Hello World!\n")
