import os, sys

cdir = os.path.dirname(__file__)
file = sys.argv[1]
path = os.path.join(cdir, file)
with open(path, 'r') as reader:
    number = int(reader.read())
number-=1
with open(path, 'w') as writer:
    writer.write(str(number))