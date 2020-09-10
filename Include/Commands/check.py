import random

a = {
    1: 'a',
    2: 'б',
    3: 'в',
    4: 'г'
}

for _ in range(45):
    print(a[random.randint(1, 4)])
    input()
