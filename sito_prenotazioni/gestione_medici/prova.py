import random
with open("nomi_italiani.txt", 'r', encoding="utf-8") as nomi:
    lines = nomi.read().splitlines()
    for i in range(50):
        myline =random.choice(lines)
        print(f"{i}: {myline}")