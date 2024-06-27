import os

cdir = os.path.dirname(__file__)
path = os.path.join(cdir, 'number.txt')
with open(path, 'r') as reader:
    number = int(reader.read())
number+=5
with open(path, 'w') as writer:
    writer.write(str(number))