import os

path = os.path.join(os.path.dirname(__file__), 'number.txt')
with open(path, 'r') as reader:
    number = int(reader.read())
print(number)
assert number == 4
# zerar
with open(path,'w') as writer:
    writer.write(str(0))