import sys


dict = {}
with open(sys.argv[1]) as f:
    txt = f.read()
    for char in txt:
        dict[char] = dict.get(char, 0) + 1

for k, v in sorted(dict.items(), key=lambda x: x[1], reverse=True):
    print(f"{k}: {v}")
